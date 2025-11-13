
from fastapi import FastAPI, Body, status, HTTPException

from .connect import client as mqtt_client
from .config import settings
from .mapping import NetworkDevices

# Init Services
app = FastAPI()

print(f"Connecting to mqtt broker on {settings.broker_hostname}:{settings.broker_port}")
mqtt_client.loop_start()

@app.put("/api/config/assoc")
def config_device_assoc(assoc: dict[str, list[str]] = Body(...)):
    print("Updating sensor mappings")
    if NetworkDevices.set_sensor_mappings(assoc):
       return
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Trying to create associations to devices that don't exist")
    
    
@app.post("/api/devices")
def get_devices():
    return {
        "sensors": NetworkDevices.get_sensor_devices(),
        "cameras": NetworkDevices.get_camera_devices()
    }


