import random
import time

from paho.mqtt import client as mqtt_client


broker = 'broker.emqx.io'
port = 1883

# This is for jetson nano
# Jetson nano will publish the result to the broker

# Connect to the topic based on the different traffic
# state as /traffic_1 and /traffic_2
# traffic_1 is the vertical road
# traffic_2 is the horizontal road

topic = "/python/5Things"
# generate client ID with pub prefix randomly
# To change the client_id to where the traffic is
client_id = "traffic_south"
# username = 'emqx'
# password = 'public'


# TODO Read the count of the car
def emergency_car():
    # If a car reach the length of 7, inform the traffic to change the light at the controller
    while true:
        is_emergency = random.randint(0, 1)
        return is_emergency

# TODO get the type of car
def car_count():
    # If a car reach the length of 7, inform the traffic to change the light at the controller
    while true:
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
    while True:
        time.sleep(1)
        
        # Return the number of car being generated
        msg = f"messages:{[car_count(), client_id, emergency_car()]"
        
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
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
    
        

    client.subscribe(topic)
    client.on_message = on_message


def run():
    client = connect_mqtt()
    client.loop_start()
    publish(client)
    client.subscribe("/python/5Things", 2)


if __name__ == '__main__':
    run()