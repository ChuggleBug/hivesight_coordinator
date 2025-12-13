import json
from ..client.connect import client as mqttClient
from ..models.config import settings
from io import BytesIO
from typing import NamedTuple, Optional
import asyncio
from PIL import Image
import imageio.v3 as iio
import numpy as np
import requests


class CameraFrame(NamedTuple):
    frame: BytesIO
    event: asyncio.Event


class CameraFrameData(NamedTuple):
    video_frame: CameraFrame
    upload_frames: list[BytesIO]


class NetworkDevices:
    """Static wrapper for managing network device collections."""

    # Static data
    _camera_devices: dict[str, CameraFrameData] = {}
    _sensor_devices: set[str] = set()
    _sensor_mappings: dict[str, list[str]] = {}

    def __new__(cls, *args, **kwargs):  # type: ignore
        raise TypeError("This is intended to be a static class")

    # Static getters
    @staticmethod
    def get_camera_devices() -> set[str]:
        return set(NetworkDevices._camera_devices.keys())

    @staticmethod
    def get_sensor_devices() -> set[str]:
        return NetworkDevices._sensor_devices

    @staticmethod
    def get_sensor_mappings() -> dict[str, list[str]]:
        return NetworkDevices._sensor_mappings

    @staticmethod
    def add_camera(device_name: str) -> bool:
        if device_name not in NetworkDevices._camera_devices:
            camera_frame_data = CameraFrameData(
                CameraFrame(
                    BytesIO(), asyncio.Event()),
                list()
            )
            NetworkDevices._camera_devices[device_name] = camera_frame_data
            return True
        return False

    @staticmethod
    def add_sensor(device_name: str) -> bool:
        if device_name not in NetworkDevices._sensor_devices:
            # Add sensor to mapping if not already
            if device_name not in NetworkDevices._sensor_mappings:
                NetworkDevices._sensor_mappings[device_name] = []
            NetworkDevices._sensor_devices.add(device_name)
            return True
        return False

    @staticmethod
    def delete_camera(device_name: str) -> bool:
        if device_name not in NetworkDevices._camera_devices:
            return False

        # Remove camera from camera set
        NetworkDevices._camera_devices.pop(device_name)

        # Remove camera from any sensor mappings
        for cameras in NetworkDevices._sensor_mappings.values():
            if device_name in cameras:
                cameras.remove(device_name)

        return True

    @staticmethod
    def delete_sensor(device_name: str) -> bool:
        if device_name not in NetworkDevices._sensor_devices:
            return False

        # Remove sensor from sensor set
        NetworkDevices._sensor_devices.remove(device_name)

        # Remove its mapping entirely
        NetworkDevices._sensor_mappings.pop(device_name, None)
        return True

    @staticmethod
    def set_sensor_mappings(new_mappings: dict[str, list[str]]) -> bool:
        for sensor, cameras in new_mappings.items():
            if sensor not in NetworkDevices._sensor_devices:
                return False
            for camera in cameras:
                if camera not in NetworkDevices._camera_devices.keys():
                    return False
        NetworkDevices._sensor_mappings = new_mappings
        return True

    @staticmethod
    def clear_all() -> None:
        NetworkDevices._camera_devices.clear()
        NetworkDevices._sensor_devices.clear()
        NetworkDevices._sensor_mappings.clear()

    @staticmethod
    def message_mappings_to_camera(device_name: str) -> None:
        sensor_list: list[str] = []
        for sensor, cameras in NetworkDevices.get_sensor_mappings().items():
            if device_name in cameras:
                sensor_list.append(sensor)
        print(f"messaging mapping/{device_name}")
        mqttClient.publish(f"mapping/{device_name}",
                           json.dumps({device_name: sensor_list}))

    @staticmethod
    async def set_latest_frame(camera_name: str, imageBytes: BytesIO) -> bool:
        if camera_name not in NetworkDevices._camera_devices:
            return False
        camera_frame = NetworkDevices._camera_devices[camera_name].video_frame
        camera_frame.frame.seek(0)
        camera_frame.frame.write(imageBytes.read())
        camera_frame.event.set()
        return True

    @staticmethod
    async def get_latest_frame(camera_name: str) -> Optional[BytesIO]:
        if camera_name not in NetworkDevices._camera_devices.keys():
            return None
        camera_frame = NetworkDevices._camera_devices[camera_name].video_frame
        await camera_frame.event.wait()
        camera_frame.event.clear()
        return camera_frame.frame

    @staticmethod
    async def add_frame_to_upload_buffer(camera_name: str, imageBytes: BytesIO) -> bool:
        if (camera_name) not in NetworkDevices._camera_devices.keys():
            return False

        NetworkDevices._camera_devices[camera_name].upload_frames.append(
            imageBytes)
        return True

    @staticmethod
    async def clear_frame_upload_buffer(camera_name: str) -> bool:
        if (camera_name) not in NetworkDevices._camera_devices.keys():
            return False

        NetworkDevices._camera_devices[camera_name].upload_frames.clear()
        return True

    @staticmethod
    async def upload_video_frames(camera_name: str, frame_rate: int) -> bool:
        if camera_name not in NetworkDevices._camera_devices:
            return False

        frames = NetworkDevices._camera_devices[camera_name].upload_frames
    
        video_buffer = BytesIO()
        with iio.imopen(video_buffer, "w", extension=".mp4", plugin="pyav") as out_file:
            out_file.init_video_stream("libx264", fps=frame_rate)
            
            for frame in frames:
                frame_data = iio.imread(frame, extension=".jpg")
                out_file.write_frame(frame_data)
        video_buffer.seek(0)

        # Now video_buffer contains the video in-memory
        # You can upload it directly using requests or any other HTTP client
        # Example with requests:
        
        url = f"http://{settings.cloud_hostname}:{settings.cloud_port}/api/video/upload"
        files = {
            "video": ("video.mp4", video_buffer, "video/mp4")
        }
        params = {"user": "user"}
        response = requests.put(url, params=params, files=files)
        response.raise_for_status()
        

        # Clear the upload buffer
        await NetworkDevices.clear_frame_upload_buffer(camera_name)
        return True


# Dummy data for testing
# NetworkDevices.add_camera("Patio")
# NetworkDevices.add_camera("Fence")
# NetworkDevices.add_camera("Kitchen")

# NetworkDevices.add_sensor("Button")
# NetworkDevices.add_sensor("Door")

# if not NetworkDevices.set_sensor_mappings({
#     "Button": [
#         "Patio",
#         "Fence"
#     ],
#     "Door": [
#         "Kitchen"
#     ]
# }):
#     print("Error setting test mappings")
