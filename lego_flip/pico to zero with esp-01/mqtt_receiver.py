import asyncio
from pybricksdev.connections import BLEPUPConnection
from paho.mqtt import client as mqtt_client

# Replace with the address of your LEGO D11 Bulldozer Powered Up Hub
hub_address = "90:84:2B:4A:CB:7E"
left_motor_port = 'A'
right_motor_port = 'B'

broker = "localhost"
topic = "lego/d11_bulldozer"

connection = None
speed_left = 0
speed_right = 0

async def main():
    global connection
    connection = await BLEPUPConnection.create(hub_address)
    await connection.connect()

    mqtt_client = mqtt_client.Client()
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message

    mqtt_client.connect(broker)
    mqtt_client.loop_start()

    try:
        while True:
            await asyncio.sleep(1)
    finally:
        mqtt_client.loop_stop()
        mqtt_client.disconnect()
        await connection.disconnect()

def on_connect(client, userdata, flags, rc):
    print(f"Connected to MQTT broker with result code {rc}")
    client.subscribe(topic)

def on_message(client, userdata, message):
