from bluedot.btcomm import BluetoothClient
from datetime import datetime
from time import sleep
from signal import pause
import json
import csv
import os

def data_received(data):

    with open(file_name, mode='a+') as latency_file:
        latency_writer = csv.writer(latency_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        latency_writer.writerow([datetime.now(), data])
        print (data)


print("Connecting to bluetooth server.")
client = BluetoothClient("raspberrypi",data_received)


count = 0
file = 'bluetooth_client_latency'
file_name = f"{file}_{count}.csv"
if os.path.isfile(file_name):
    while os.path.isfile(file_name):
        if not os.path.isfile(file_name):
            break
        
        count = count + 1
        file_name = f"{file}_{count}.csv"

print("Sending")
try:
    while True:
        now = datetime.now()
        current_time = now.strftime('%H:%M:%S.%f')[:-3]
        print(current_time)
        client.send("{time} {payload}".format(
            time=current_time,
            payload="{\"enabled\": true, \"direction\": \"west\"}" 
            ))
        sleep(1)
finally:
    c.disconnect()

