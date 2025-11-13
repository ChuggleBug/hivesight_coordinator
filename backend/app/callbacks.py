
from paho.mqtt.client import Client, MQTTMessage
from typing import Any
from pathlib import Path

from .mapping import NetworkDevices

def on_connect_cb(client: Client, userdata: Any, flags: dict, reasonCode: int, properties: Any = None): # type: ignore
    print("Connected to broker!")
    
def on_message_cb(client: Client, userdata: Any, msg: MQTTMessage):  # type: ignore
    print(f"Message on {msg.topic} arrived")

def on_sensor_cb(client: Client, userdata: Any, msg: MQTTMessage):  # type: ignore
    sensor_topic = Path(msg.topic).name
    print(f"{sensor_topic} triggered an event")
    for sensor in NetworkDevices.get_sensor_devices():
        if (sensor_topic == sensor):
            print(f"Capturing feed for cameras {NetworkDevices.get_sensor_mappings()[sensor_topic]}")
            return
    print(f"{sensor_topic} is currently not in the network")
    