# publisher
import paho.mqtt.client as mqtt

client = mqtt.Client()
client.connect('192.168.1.85', 1883)

while True:
    client.publish("LINTANGtopic/test", input('Message : '))