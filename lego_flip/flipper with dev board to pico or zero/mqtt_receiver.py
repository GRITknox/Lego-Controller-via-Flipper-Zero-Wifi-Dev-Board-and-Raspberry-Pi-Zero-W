#runs on pi zero w
#make sure you replace your hub_address variable

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
    payload = message.payload.decode()

    if payload == "forward":
        speed_left = 50
        speed_right = 50
    elif payload == "backward":
        speed_left = -50
        speed_right = -50
    elif payload == "left":
        speed_left = -50
        speed_right = 50
    elif payload == "right":
        speed_left = 50
        speed_right = -50
    elif payload == "stop":
        speed_left = 0
        speed_right = 0
    elif payload == "toggle_front_blade":
        # Add code to control the front blade
        pass
    elif payload == "toggle_back_ripper":
        # Add code to control the back ripper
        pass
    else:
        return

    # Update motor speeds
    asyncio.run_coroutine_threadsafe(
        connection.send_motor_msg(left_motor_port, speed_left), asyncio.get_event_loop())
    asyncio.run_coroutine_threadsafe(
        connection.send_motor_msg(right_motor_port, speed_right), asyncio.get_event_loop())

if __name__ == "__main__":
    asyncio.run(main())
