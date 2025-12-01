# routes/devices.py

from fastapi import APIRouter, Body, status, HTTPException, File, UploadFile, Query, Request
from typing import Dict
from ..models.mapping import NetworkDevices
from PIL import Image, UnidentifiedImageError
import io

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
    # Read raw bytes from the request body
    image_bytes = await request.body()
    try:
        image = Image.open(io.BytesIO(image_bytes))
    except UnidentifiedImageError:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail="Could not process data bytes into image"
        )
    image.save(f"{device}.jpg")
