
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from paho.mqtt.enums import MQTTErrorCode
from .client.connect import client as mqtt_client
from .models.config import settings

from .routes.user import router as user_routes
from .routes.device import router as device_routes
import time

# Init Services
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,  # Set to True if you need to allow cookies/authorization headers
    allow_methods=["*"],     # This allows all HTTP methods
    allow_headers=["*"],     # This allows all headers
)

print(f"Connecting to mqtt broker on {settings.broker_hostname}:{settings.broker_port}")

if mqtt_client.loop_start() != MQTTErrorCode.MQTT_ERR_SUCCESS:
    print(f"Failed to connect to broker. Retrying...")
    time.sleep(1)

app.include_router(user_routes, prefix="/api/user")
app.include_router(device_routes, prefix="/api/device")
