# Lego-Controller-via-Flipper-Zero-Wifi-Dev-Board-and-Raspberry-Pi-Pico-W
This is for the D11 Lego Bulldozer, but should work for any with proper formatting.

This can be done without the Flipper Zero WiFi dev board.  You would need to purchase a 433 MHz RF module and pair it with any Pi or Arduino type device.

Make sure you have the necessary libraries and software installed on both devices. For the Flipper Zero, you need the MQTT and Wi-Fi libraries (mqtt and wifi). For the Raspberry Pi Zero W, you need the Paho MQTT library (paho-mqtt) and Pybricks library (pybricksdev).

Ensure you have properly configured both scripts with your Wi-Fi SSID, password, and MQTT broker's address (which should be the IP address or hostname of your Raspberry Pi Zero W). Once you have done this, you should be able to control the LEGO D11 Bulldozer using the Flipper Zero with the Wi-Fi dev board and Raspberry Pi Zero W.

Trying to get the pico to work as well but since it does not support low energy bluetooth its probably not going to happen without another module.  Pico code is in there but I would tread lightly.  

Backups are your friend.

@GRITknox on twitter if you have any questions.
