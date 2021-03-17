import random
import time

from paho.mqtt import client as mqtt_client
import IOTtrafficlights as traffic_light


broker = 'broker.emqx.io'
port = 1883

# This is for jetson nano
# Jetson nano will publish the result to the broker

# Connect to the topic based on the different traffic
# state as /traffic_1 and /traffic_2
# traffic_1 is the vertical road
# traffic_2 is the horizontal road

topic = "/python/5Things"
topic_recieved = "/python/5Things/traffic2"
# generate client ID with pub prefix randomly
# To change the client_id to where the traffic is
client_id = "south"
# username = 'emqx'
# password = 'public'

PUBLISH_FLAG = True


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
    while PUBLISH_FLAG:
        time.sleep(5)
        
        # Return the number of car being generated
        msg = f"messages:[{car_count()}, '{client_id}', {emergency_car()}]"
        
        # Publis the message
        result = client.publish(topic, msg)
        # result: [0, 1]
        status = result[0]
        if status == 0:
            print(f"Send `{msg}` to topic `{topic}`")
        else:
            print(f"Failed to send message to topic {topic}")
        msg_count += 1
        

def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        PUBLISH_FLAG = False
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
        # Split the message
        message = msg.split(":")
        # Check the condition of the traffic
        traffic_status = literal_eval(message[1])
        # If the traffic condition is true
        # Vertical traffic light should be green
        if traffic_status:
            traffic_light.green()
            print("Vertical")
        else:
            traffic_light.red()
            print("Horizontal")
        
    
        

    client.subscribe(topic_recieved)
    client.on_message = on_message


def run():
    client = connect_mqtt()
    client.loop_start()
    publish(client)
    print("here")
    client.subscribe(topic_recieved, 2)


if __name__ == '__main__':
    run()