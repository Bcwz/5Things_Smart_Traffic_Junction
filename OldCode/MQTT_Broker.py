import random

from paho.mqtt import client as mqtt_client
from ast import literal_eval
import time


broker = 'broker.emqx.io'
port = 1883

# TODO Chnage the traffic light
topic = "/python/5Things/traffic2"
topic_received = "/python/5Things"
# generate client ID with pub prefix randomly
# client_id = f'python-mqtt-{random.randint(0, 100)}'
client_id = "traffic_controller"

# username = 'emqx'
# password = 'public'

# index number 1 is the vertical side
# index number 2 is the horizontal side
traffic_1 = ["north", "south"]
traffic_2 = ["east", "west"]

# True : Set the vertical to be green
# False : Set the vertical to be red
traffic_open = True

def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    # client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

# http://www.steves-internet-guide.com/into-mqtt-python-client/
def on_message(client: mqtt_client):
    def on_message(client, userdata, msg):
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
        traffic_condition(msg.payload.decode())
        

    client.subscribe(topic_received)
    client.on_message = on_message

def publish(client, traffic_open):
    
    msg_count = 0
    
    # Return the number of car being generated
    msg = f"messages:{traffic_open}"
    
    # Publis the message
    result = client.publish(topic, msg)
    print(result)
    # result: [0, 1]
    status = result[0]
    if status == 0:
        print(f"Send `{msg}` to topic `{topic}`")
    else:
        print(f"Failed to send message to topic {topic}")
    msg_count += 1
        

def traffic_condition(msg):
    message = msg.split(":")
    # Get the second array as it contain our array of things
    # array[0] is the length of car
    # array[1] is the direction of the car : clientid
    # array[2] is the emergency vehicle
    # Convert string to array
    traffic_status = literal_eval(message[1])
    
    if traffic_status[1] in traffic_1:
        if traffic_status[2] is True or traffic_status[0] >= 7:
            # Set the green light of traffic for vertical
            traffic_condition = True
            print("Allow Vertical to pass")
            # TODO Change return to publish
            publish(client, traffic_condition)
            # return traffic_condition
        
    elif traffic_status[1] in traffic_2:
        if traffic_status[2] is True or traffic_status[0] >= 7:
             # Set the green light of traffic for horizontal
            traffic_condition = False
            print("Allow horizontal to pass")
            # TODO Change return to publish
            publish(client, traffic_condition)
        
    else:
        print("No changes is made")
        return traffic_condition


# Set this as global so that the client can be read by
# other function
client = connect_mqtt()
on_message(client)
client.loop_forever()


# def run():
#     client = connect_mqtt()
#     on_message(client)
#     client.loop_forever()


if __name__ == '__main__':
    run()