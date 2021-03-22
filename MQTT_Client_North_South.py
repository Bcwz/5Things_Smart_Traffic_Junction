import random
import time
from time import sleep

from paho.mqtt import client as mqtt_client
import IOTtrafficlights as traffic_light
from ast import literal_eval


broker = 'broker.emqx.io'
port = 1883

# This is for jetson nano
# Jetson nano will publish the result to the broker

# Connect to the topic based on the different traffic
# state as /traffic_1 and /traffic_2
# traffic_1 is the vertical road
# traffic_2 is the horizontal road

topic = [("/python/5Things/traffic2", 2), ("/python/5Things/enable",2), ("/python/5Things/traffic_north_south",2), ("/python/5Things/traffic_east_west",2)]
# generate client ID with pub prefix randomly
# To change the client_id to where the traffic is
client_id = "traffic_north_south"
# username = 'emqx'
# password = 'public'

PUBLISH_FLAG = True
ENABLE = False



# TODO Read the count of the car
def emergency_car():
    # If a car reach the length of 7, inform the traffic to change the light at the controller
    while True:
        is_emergency = random.randint(0, 1)
        if is_emergency:
            return True
        else:
            return False


# TODO get the type of car
def car_count():
    # If a car reach the length of 7, inform the traffic to change the light at the controller
    while True:
        count = random.randint(0, 10)
        return count


def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    # Client id is set here
    client = mqtt_client.Client(client_id)
    # client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def publish(client):
    msg_count = 0
    
    time.sleep(5)
    
    # Return the number of car being generated
    msg = f"'car_count':[{car_count()}, '{client_id}', {False}]"
    
    # Publis the message
    result = client.publish(topic[1][0], msg, 2)
    # result: (0, 1)
    status = result[0]
    if status == 0:
        print(f"Send `{msg}` to topic `{topic[1][0]}`")
    else:
        print(f"Failed to send message to topic {topic}")
    msg_count += 1

        

def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
        message = msg.payload.decode()
        # Split the message
        message_check_condition = message.split(":")
        # Check the condition of the traffic
        traffic_status = literal_eval(message_check_condition[1])
        if msg.topic == topic[2][0]:
            if traffic_status:
                print("Smart Traffic Enable")
                enable_traffic(True)
            else:
                print("Smart Traffic Not Enable")
                enable_traffic(False)
            sleep(3)
            publish(client)
        else:
            if ENABLE:
                # If the traffic condition is true
                # Vertical traffic light should be green
                if traffic_status is True:
                    change_traffic_state()
                    print("Vertical")
                else:
                    traffic_light.red()
                    print("Horizontal")
                # Repeat the whole process again
                publish(client)
                #print("message topic=",msg.topic)
                #print("message qos=",msg.qos)
                #print("message retain flag=",msg.retain)
            else:
                print("Enable False")
                sleep(3)
                publish(client,)
              
        
    client.subscribe([topic[0], topic[2]])
    client.on_message = on_message
    publish(client)
    
def change_traffic_state():
    traffic_light.red()
    sleep(3)
    traffic_light.orange()
    sleep(3)
    traffic_light.green()   

def on_log(client, userdata, level, buf):
    print("message:" + str(buf))

def enable_traffic(status):
    if status:
        ENABLE = True
    else:
        ENABLE = False


enable = enable_traffic(False)

client = connect_mqtt()
client.on_log=on_log
subscribe(client)
client.loop_forever()


#if __name__ == '__main__':
#    ENABLE = False
