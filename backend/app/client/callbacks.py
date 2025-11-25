
from paho.mqtt.client import Client, MQTTMessage
from typing import Any

def on_connect_cb(client: Client, userdata: Any, flags: dict, reasonCode: int, properties: Any = None): # type: ignore
    print("Connected to broker!")
    
def on_message_cb(client: Client, userdata: Any, msg: MQTTMessage):  # type: ignore
    print(f"Message on {msg.topic} arrived")
    