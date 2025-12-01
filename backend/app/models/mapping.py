import json
from ..client.connect import client as mqttClient

class NetworkDevices:
    """Static wrapper for managing network device collections."""

    # Static data
    _camera_devices: set[str] = set()
    _sensor_devices: set[str] = set()
    _sensor_mappings: dict[str, list[str]] = {}

    def __new__(cls, *args, **kwargs): # type: ignore
        raise TypeError("This is intended to be a static class")

    # Static getters
    @staticmethod
    def get_camera_devices() -> set[str]:
        return NetworkDevices._camera_devices

    @staticmethod
    def get_sensor_devices() -> set[str]:
        return NetworkDevices._sensor_devices

    @staticmethod
    def get_sensor_mappings() -> dict[str, list[str]]:
        return NetworkDevices._sensor_mappings

    @staticmethod
    def add_camera(device_name: str) -> bool:
        if device_name not in NetworkDevices._camera_devices:
            NetworkDevices._camera_devices.add(device_name)
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
        NetworkDevices._camera_devices.remove(device_name)

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
                if camera not in NetworkDevices._camera_devices:
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
        mqttClient.publish(f"mapping/{device_name}", json.dumps({device_name: sensor_list}))


# Dummy data for testing
NetworkDevices.add_camera("Patio")
NetworkDevices.add_camera("Fence")
NetworkDevices.add_camera("Kitchen")

NetworkDevices.add_sensor("Button")
NetworkDevices.add_sensor("Door")

if not NetworkDevices.set_sensor_mappings({
    "Button": [
        "Patio",
        "Fence"
    ],
    "Door": [
        "Kitchen"
    ]
}):
    print("Error setting test mappings")
