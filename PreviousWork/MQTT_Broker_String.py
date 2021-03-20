import random

from paho.mqtt import client as mqtt_client
from ast import literal_eval
import time

import json

broker = 'broker.emqx.io'
port = 1883

# TODO Chnage the traffic light
topic = [("/python/5Things/traffic_north_south",2), ("/python/5Things/traffic_east_west",2)]
# topic_received =
# generate client ID with pub prefix randomly
# client_id = f'python-mqtt-{random.randint(0, 100)}'
client_id = "traffic_controller"

# username = 'emqx'
# password = 'public'

# index number 1 is the vertical side
# index number 2 is the horizontal side
traffic = ["traffic_north_south", "traffic_east_west"]

# Number of traffic is being connected
connected_devices = []

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
def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        m_decode=str(msg.payload.decode("utf-8","ignore"))
        
        
        
        
        print(f"Received `{message}` from `{msg.topic}` topic")
       
        # if len(connected_devices) == 4 and all(devices in (traffic_1 + traffic_2) for devices in connected_devices):
        if len(connected_devices) == 2:
            traffic_condition(msg.payload.decode())
        else:
            split_message = message.split(":")
            paramter = literal_eval(split_message[1])
            if paramter[1] not in connected_devices:
                connected_devices.append(paramter[1])
                print(connected_devices)
            
            publish(client, topic[2][0], False)
            
  
        # print("message topic=",msg.topic)
        # print("message qos=",msg.qos)
        # print("message retain flag=",msg.retain)
        
    client.subscribe(topic[1])
    client.on_message = on_message

def publish(client, topic, message):
    
    msg_count = 0
    
    # Return the number of car being generated
    msg = f"messages:{message}"
    
    # Publis the message
    result = client.publish(topic, msg, 2)
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
    print(message)
    # Get the second array as it contain our array of things
    # array[0] is the length of car
    # array[1] is the direction of the car : clientid
    # array[2] is the emergency vehicle
    # Convert string to array
    traffic_status = literal_eval(message[1])
    
    if traffic_status[1] == traffic[0]:
        if traffic_status[2] is True or traffic_status[0] >= 7:
            # Set the green light of traffic for vertical
            traffic_condition = True
            print("Allow Vertical to pass")
            # TODO Change return to publish
            publish(client,topic[0][0], traffic_condition)
            # return traffic_condition
        
    elif traffic_status[1] == traffic[1]:
        if traffic_status[2] is True or traffic_status[0] >= 7:
             # Set the green light of traffic for horizontal
            traffic_condition = False
            print("Allow horizontal to pass")
            # TODO Change return to publish
            publish(client,topic[0][0], traffic_condition)
        
    else:
        publish(client,topic[0][0], traffic_condition)
        print("No changes is made")
        
def string_to_json(m_decode):
    return json.loads(m_decode)

def json_to_string(m_decode):
    return json.dumps(m_decode)
    
        
    
def on_log(client, userdata, level, buf):
    print("message:" + str(buf))
    print("userdata:" + str(userdata))
    print("level:" + str(level))


# Set this as global so that the client can be read by
# other function
client = connect_mqtt()
subscribe(client)
client.loop_forever()


# def run():
#     client = connect_mqtt()
#     on_message(client)
#     client.loop_forever()


# if __name__ == '__main__':
#     run()