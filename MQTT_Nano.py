# publisher
import paho.mqtt.client as mqtt

client_id = "traffic_controller"
client = mqtt.Client(client_id)
client.connect('172.30.138.65', 1883)
# client.username_pw_set(client_id)

while True:
    client.publish("5Things/traffic_change", input('Message : '))