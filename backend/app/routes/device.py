# routes/devices.py

from fastapi import APIRouter, Body, status, HTTPException, Request, Header
from typing import Dict, Annotated
from ..models.mapping import NetworkDevices
from PIL import Image, UnidentifiedImageError
from starlette.requests import ClientDisconnect
import io
import asyncio

router = APIRouter(
    tags=["Devices"]
)


@router.put("/register", status_code=status.HTTP_204_NO_CONTENT, summary="Register a device")
def register_device(
    register_info: Dict[str, str] = Body(
        ...,
        examples=[
            {
                "name": "button",
                "type": "sensor"
            },
            {
                "name": "patio",
                "type": "camera"
            },
        ]
    )
):
    try:
        print(f"Device attempting to connect. Name: {register_info['name']}")
        if register_info['type'] not in ["camera", "sensor"]:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Type must be either 'camera' or 'sensor'"
            )

        device_name: str = register_info["name"]
        device_type: str = register_info["type"]
        if device_type == "camera":
            NetworkDevices.add_camera(device_name)
            # Additionally needs to provide all devices to respond to if a camera
            NetworkDevices.message_mappings_to_camera(device_name)
        elif device_type == "sensor":
            NetworkDevices.add_sensor(register_info['name'])
    except KeyError:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Missing required fields"
        )


@router.put("/stream", status_code=status.HTTP_204_NO_CONTENT, summary="Upload latest image capture")
async def stream_device(device: str, request: Request):
    if device not in NetworkDevices.get_camera_devices():
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Device not registered in network"
        )
    # Read raw bytes from the request body
    image_bytes = await request.body()
    try:
        image = Image.open(io.BytesIO(image_bytes))
    except UnidentifiedImageError:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail="Could not process data bytes into image"
        )
    # Save image as encoded JPEG for later use
    buffered = io.BytesIO()
    image.save(buffered, format="JPEG")
    buffered.seek(0)

    # Device is in the network as it was checked
    if await NetworkDevices.set_latest_frame(device, buffered):
        return

    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
    )


@router.post("/upload", status_code=status.HTTP_204_NO_CONTENT)
async def upload_frame(
    device: str,
    request: Request,
    first_frame: Annotated[bool | None, Header()],
    upload_complete: Annotated[bool | None, Header()],
    event_timestamp: Annotated[int | None, Header()],
):
    if (upload_complete):
        print("finished uploading", device)
        if (device not in NetworkDevices.get_camera_devices()):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Device not registered in network"
            )

        # Handle logic for converting video and uploading to server
        asyncio.create_task(NetworkDevices.upload_video_frames(device, 6))
        return

    # Clear out current buffer
    if (first_frame):
        print("first frame for", device)
        if not (await NetworkDevices.clear_frame_upload_buffer(device)):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Device not registered in network"
            )

    # Transform body to usable bytes for for later uploading
    try:
        image_bytes = await request.body()
        image = Image.open(io.BytesIO(image_bytes))
    except (UnidentifiedImageError, ClientDisconnect):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail="Could not process data bytes into image"
        )
    # Save image as encoded JPEG for later use
    buffered = io.BytesIO()
    image.save(buffered, format="JPEG")
    buffered.seek(0)

    print("adding frame to", device)
    if not (await NetworkDevices.add_frame_to_upload_buffer(device, buffered)):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Device not registered in network"
        )
