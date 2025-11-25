import paho.mqtt.client as paho
# from paho.mqtt.enums import MQTTErrorCode

from ..models.config import settings
from .callbacks import *

client = paho.Client(client_id="", userdata=None, protocol=paho.MQTTv5)
client.on_connect = on_connect_cb

client.connect(settings.broker_hostname, settings.broker_port)

client.on_message = on_message_cb

