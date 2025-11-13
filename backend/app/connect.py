import paho.mqtt.client as paho

from .config import settings
from .callbacks import *

client = paho.Client(client_id="", userdata=None, protocol=paho.MQTTv5)
client.on_connect = on_connect_cb

client.connect(settings.broker_hostname, settings.broker_port)

client.subscribe("sensor/+", qos=1)

client.on_message = on_message_cb
client.message_callback_add("sensor/+", on_sensor_cb)