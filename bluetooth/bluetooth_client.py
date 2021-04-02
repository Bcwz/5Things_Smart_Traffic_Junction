from bluedot.btcomm import BluetoothClient
from datetime import datetime
from time import sleep
from signal import pause
import json

def data_received(data):
    print (data)
print("Connecting to bluetooth server.")
client = BluetoothClient("raspberrypi",data_received)

print("Sending")
try:
    while True:
        now = datetime.now()
        current_time = now.strftime('%H:%M:%S.%f')[:-3]
        client.send("{time} {payload}".format(
            time=current_time,
            payload="{\"enabled\": true, \"direction\": \"west\"}" 
            ))
        sleep(1)
finally:
    c.disconnect()