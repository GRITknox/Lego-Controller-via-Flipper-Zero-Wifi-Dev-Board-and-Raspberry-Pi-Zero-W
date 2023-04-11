#runs on pico with an esp-01 wi-fi module
#pybricks does not play well with the pico since pico does not use BLE
#the umqtt.simple library is required

import machine
import time
import ubinascii
from simple import MQTTClient
from pybricksdev.connections import BLEPUPConnection

# Replace with the address of your LEGO D11 Bulldozer Powered Up Hub
hub_address = "90:84:2B:4A:CB:7E"
left_motor_port = 'A'
right_motor_port = 'B'

# Replace with your Wi-Fi SSID, password, and Raspberry Pi MQTT broker address
SSID = "your_ssid"
PASSWORD = "your_password"
MQTT_BROKER = "raspberrypi.local"
MQTT_TOPIC = "lego/d11_bulldozer"

# UART for communication with the ESP-01
uart = machine.UART(0, baudrate=115200, tx=machine.Pin(1), rx=machine.Pin(0))

# Connect to Wi-Fi
def connect_wifi():
    uart.write("AT+RST\r\n")
    time.sleep(1)
    uart.write("AT+CWMODE=1\r\n")
    time.sleep(1)
    uart.write("AT+CWJAP=\"" + SSID + "\",\"" + PASSWORD + "\"\r\n")
    time.sleep(5)

# Set up MQTT client
def setup_mqtt():
    client_id = ubinascii.hexlify(machine.unique_id())
    mqtt_client = MQTTClient(client_id, MQTT_BROKER)
    mqtt_client.set_callback(on_message)
    mqtt_client.connect()
    mqtt_client.subscribe(MQTT_TOPIC)
    return mqtt_client

# Connect to the LEGO Powered Up Hub
async def connect_lego_hub():
    connection = await BLEPUPConnection.create(hub_address)
    await connection.connect()
    return connection

# MQTT message callback
def on_message(topic, payload):
    payload = payload.decode()

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

# Main function
async def main():
    connect_wifi()
    mqtt_client = setup_mqtt()
    connection = await connect_lego_hub()

    while True:
        mqtt_client.check_msg()
        await asyncio.sleep(1)

# Run the script
asyncio.run(main())
