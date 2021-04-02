from bluedot.btcomm import BluetoothServer
from time import sleep
from signal import pause
from datetime import datetime

def data_received(data):
    # Get current time
    now = datetime.now().strftime("%H:%M:%S.%f")
    current_time = datetime.strptime(now,"%H:%M:%S.%f")
    # Convert the payload time to a datetime object
    payload_time = datetime.strptime(data[0:12], '%H:%M:%S.%f')
    latency=current_time-payload_time
    print("Data from client: ", data,"\nLatency: ",latency)
    server.send("Data received. Latency: {}".format(latency))

def client_connected():
    print("Client connected")

def client_disconnected():
    print("Client disconnected")

print("Bluetooth server is starting.")
server = BluetoothServer(
    data_received,
    auto_start = False,
    when_client_connects = client_connected,
    when_client_disconnects = client_disconnected)

server.start()
print("MAC Address: ", server.server_address)
print("Waiting for connection")

try:
    pause()
except KeyboardInterrupt as e:
    print("cancelled by user")
finally:
    print("stopping")
    server.stop()
print("stopped")