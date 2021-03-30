from threading import Thread
import time
import random
from threading import Timer

# publisher
from paho.mqtt import client as mqtt_client
import json

broker = '172.30.138.214'
port = 1883

# # TODO Chnage the traffic light
topic = [("5Things/traffic_change",2), ("5Things/traffic_condition",2)]

# # generate client ID with pub prefix randomly
client_id = "north"
traffic_lookout = ["north", "south"]
# traffic_lookout = ["west", "east"]

# Timer
# Pass in the timer number
class RepeatTimer(Timer):
    def run(self):
        # If the interval is not finish, run the function
        while not self.finished.wait(self.interval):
            self.function(*self.args, **self.kwargs)


class TrafficStatus:
    def __init__(self, status):
        self.status = status
        
    def change(self, state):
        self.status = state

class RoadCar:
    def __init__(self, emergency = None, numOfCar = None):
        self.emergency = emergency
        self.numOfCar =numOfCar
        
    def setRoadCount(self, numOfCar):
        self.numOfCar = numOfCar
            
    def setRoadEmegency(self, emergency):
        self.emergency = emergency


class SmartTraffic:
    def __init__(self, enabled, time_extended):
        self.enabled = enabled
        self.time_extended =time_extended
        
    def setSmartTraffic(self, enabled):
        self.enabled = enabled
            
    def setTimeExtended(self, time_extended):
        self.time_extended = time_extended
        
        
sTraffic = SmartTraffic(False, 0)


def car_count(roadStatus):
    # If a car reach the length of 7, inform the traffic to change the light at the controller
    # while True:
    count = random.randint(0, 10)
    print(count)
    roadStatus.setRoadCount(count)
    
def emergency_bool(roadStatus):
    # If a car reach the length of 7, inform the traffic to change the light at the controller
    # while True:
    count = random.randint(0,10)
    print(count)
    if count == 0:
        roadStatus.setRoadEmegency(True)

def check_traffic_condition(status):
    # while True:
    if status["direction"] in traffic_lookout:
        sTraffic.setSmartTraffic(True)
        sTraffic.setTimeExtended(status["time_extended"])
 
        
def transit_green_to_red():
    print("Amber")
    time.sleep(3)
    print("Red")


def transit_red_to_green():
    print("Traffic is now Green")

def reset():
    sTraffic.setSmartTraffic(False)
    sTraffic.setTimeExtended(0)

def normal_traffic(trafficStatus):

    # If this is traffic turn to green
    if trafficStatus.status is True:
        transit_red_to_green()
        
        if sTraffic.enabled is True:
            print("Smart Traffic Enabled")
            time.sleep(sTraffic.time_extended)
            reset()
            print("Smart Traffic Disabled")
            
        # Traffic prepare to change to red after the next timing
        print(sTraffic.enabled)
        trafficStatus.change(False)
        # transit_red_to_green()
    else:
        transit_green_to_red()
        trafficStatus.change(True)
        

# The fixed timing for time extension
# TIME_EXTENSION = 30

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
        # print(f"Received `{m_decode}` from `{msg.topic}` topic")
        
        m_in=string_to_json(m_decode) #decode json data
        check_traffic_condition(m_in) 

           
    client.subscribe(topic[1])
    client.on_message = on_message
    
    
def string_to_json(m_decode):
    return json.loads(m_decode)

        
if __name__ == "__main__":
    try:
        tStatus = TrafficStatus(True)
        print("Red")
        timer = RepeatTimer(3,normal_traffic,args=[tStatus])
        timer.start()
        
        
        client = connect_mqtt()
        subscribe(client)
        client.loop_forever()
        
    except KeyboardInterrupt:
        timer.cancel()
