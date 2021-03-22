# publisher
from paho.mqtt import client as mqtt_client
import json

broker = '192.168.1.85'
port = 1883

# # TODO Chnage the traffic light
topic = [("5Things/traffic_change",2), ("5Things/traffic_condition",2)]

# # generate client ID with pub prefix randomly
client_id = "traffic_controller"

# Connection to the broker
def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        # If connection is connected
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client()
    # client.username_pw_set(client_id, "123")
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        m_decode=str(msg.payload.decode("utf-8","ignore"))    
        print(f"Received `{m_decode}` from `{msg.topic}` topic")
        
    client.subscribe(topic[0])
    client.on_message = on_message

client = connect_mqtt()
subscribe(client)
client.loop_forever()