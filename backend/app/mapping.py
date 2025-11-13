class NetworkDevices:
    """Static wrapper for managing network device collections."""

    # Static data
    camera_devices: set[str] = set()
    sensor_devices: set[str] = set()
    sensor_mappings: dict[str, list[str]] = {}

    def __new__(cls, *args, **kwargs):
        raise TypeError("This is intended to be a static class")

    # Static getters
    @staticmethod
    def get_camera_devices() -> set[str]:
        return NetworkDevices.camera_devices

    @staticmethod
    def get_sensor_devices() -> set[str]:
        return NetworkDevices.sensor_devices

    @staticmethod
    def get_sensor_mappings() -> dict[str, list[str]]:
        return NetworkDevices.sensor_mappings

    @staticmethod
    def add_camera(device_name: str) -> None:
        NetworkDevices.camera_devices.add(device_name)

    @staticmethod
    def add_sensor(device_name: str) -> None:
        NetworkDevices.sensor_devices.add(device_name)
        
    @staticmethod
    def delete_camera(device_name: str) -> bool:
        if device_name not in NetworkDevices.camera_devices:
            return False

        # Remove camera from camera set
        NetworkDevices.camera_devices.remove(device_name)

        # Remove camera from any sensor mappings
        for cameras in NetworkDevices.sensor_mappings.values():
            if device_name in cameras:
                cameras.remove(device_name)

        return True

    @staticmethod
    def delete_sensor(device_name: str) -> bool:
        if device_name not in NetworkDevices.sensor_devices:
            return False

        # Remove sensor from sensor set
        NetworkDevices.sensor_devices.remove(device_name)

        # Remove its mapping entirely
        NetworkDevices.sensor_mappings.pop(device_name, None)
        return True

    @staticmethod
    def set_sensor_mappings(new_mappings: dict[str, list[str]]) -> bool:
        for sensor, cameras in new_mappings.items():
            if sensor not in NetworkDevices.sensor_devices:
                return False
            for camera in cameras:
                if camera not in NetworkDevices.camera_devices:
                    return False
        NetworkDevices.sensor_mappings = new_mappings
        return True

    @staticmethod
    def clear_all() -> None:
        NetworkDevices.camera_devices.clear()
        NetworkDevices.sensor_devices.clear()
        NetworkDevices.sensor_mappings.clear()


# Dummy data for testing
NetworkDevices.add_camera("patio")
NetworkDevices.add_camera("fence")
NetworkDevices.add_camera("kitchen")

NetworkDevices.add_sensor("button")
NetworkDevices.add_sensor("door")

NetworkDevices.set_sensor_mappings({
    "button": [
        "patio",
        "fence"
    ],
    "door": [
        "kitchen"
    ]
})