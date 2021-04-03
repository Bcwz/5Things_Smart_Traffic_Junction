from threading import Thread
import time
import random
from threading import Timer
import IOT_Color as traffic_light
from datetime import date

# publisher
from paho.mqtt import client as mqtt_client
import json
import datetime

broker = '192.168.1.85'
port = 1883

FLAG_SMART_TRAFFIC = 0
ENABLE_DIRECTION_TRAFFIC = 1
DISABLE_DIRECTION_TRAFFIC = 2

# # TODO Chnage the traffic light
topic = [("5Things/traffic_change",2), ("5Things/traffic_condition",2), ("5Things/start_stop",2), ("5Things/set_traffic", 2)]

# Set your client id
client_id = "east"
# client_id = "north"
traffic_lookout = ["west", "east"]
# traffic_lookout = ["north", "south"]



# Timer
# Pass in the timer number
class RepeatTimer(Timer):        
    def run(self):
        # If the interval is not finish, run the function
        while not self.finished.wait(self.interval):
            self.function(*self.args, **self.kwargs)
                    

# Set the traffic status
class TrafficStatus:
    def __init__(self, status):
        self.status = status
        
    def change(self, state):
        self.status = state

# Set the status of the road
class RoadCar:
    def __init__(self, emergency = None, numOfCar = None):
        self.emergency = emergency
        self.numOfCar =numOfCar
        
    def setRoadCount(self, numOfCar):
        self.numOfCar = numOfCar
            
    def setRoadEmegency(self, emergency):
        self.emergency = emergency

# Set the smart traffic
class SmartTraffic:
    def __init__(self, enabled, time_extended):
        self.enabled = enabled
        self.time_extended =time_extended
        
    def setSmartTraffic(self, enabled):
        self.enabled = enabled
            
    def setTimeExtended(self, time_extended):
        self.time_extended = time_extended
        
class EnableTraffic:
    def __init__(self, enabled = False, timer = None):
        self.enabled = enabled
        self.timer = timer
    
    def setTimer(self, timer):
        self.timer = timer
        
    def setTraffic(self, enabled):
        self.enabled = enabled
            
# Declare the traffic
sTraffic = SmartTraffic(FLAG_SMART_TRAFFIC, 0)
traffic_enabled = EnableTraffic()
trafficStatus = TrafficStatus(False)


# Check the current traffic condition from topic
# ("5Things/set_traffic", 2)
def check_traffic_condition(status):
    # while True:

    if status["direction"] in traffic_lookout:
        if trafficStatus.status is True:
            sTraffic.setSmartTraffic(ENABLE_DIRECTION_TRAFFIC)
        else:
            traffic_enabled.timer.cancel()
            normal_traffic()
            start_time(trafficStatus.status)

    else:
        if trafficStatus.status is False:
            sTraffic.setSmartTraffic(DISABLE_DIRECTION_TRAFFIC)
        else:
            traffic_enabled.timer.cancel()
            normal_traffic()
            start_time(trafficStatus.status)
            
    
    sTraffic.setTimeExtended(status["time_extended"] + sTraffic.time_extended)
            
        
def reset():
    sTraffic.setSmartTraffic(FLAG_SMART_TRAFFIC)
    sTraffic.setTimeExtended(0)

def normal_traffic(): 
   
    now = datetime.datetime.now()
    # dd/mm/YY H:M:S
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

    print("Start =", dt_string) 
    if traffic_enabled.timer.finished:
        if sTraffic.enabled is not FLAG_SMART_TRAFFIC:
            # Traffic is currently Green and want to transit to red
            if sTraffic.enabled == ENABLE_DIRECTION_TRAFFIC and trafficStatus.status is True:
                traffic_light.purple()
                extend_smart_traffic()
                reset()

            # Traffic is currently Red and want to transit to green
            elif sTraffic.enabled == DISABLE_DIRECTION_TRAFFIC and trafficStatus.status is False:
                traffic_light.blue()
                extend_smart_traffic()
                reset()

    # print(f'{sTraffic.enabled} ,'{}' ')

    # If this is traffic turn to green
    if trafficStatus.status is True:
        transit_red_to_green()
        trafficStatus.change(False)

    else:
        transit_green_to_red()
        trafficStatus.change(True)
 
    
        
    
    print("End =", dt_string)	

def extend_smart_traffic():
            # print("Smart Traffic Enabled")
    time.sleep(sTraffic.time_extended)
    
    if sTraffic.enabled is True:
        sTraffic.setSmartTraffic(FLAG_SMART_TRAFFIC)
        # run_smart_traffic()
    
    else:
        reset()
    

def transit_green_to_red():
    traffic_light.orange()
    # print("Amber")
    time.sleep(3)
    traffic_light.red()
    time.sleep(3)
    # print("Red")

def transit_red_to_green():
    time.sleep(6)
    traffic_light.green()
    # print("Traffic is now Green")



def start_traffic(status):
    if status["direction"] in traffic_lookout:
        start_time(True)
        traffic_light.red()
        # print("Red")
    else:
        start_time(False)
        traffic_light.green()
        # print("Green")
        
    traffic_enabled.setTraffic(True)

        
def string_to_json(m_decode):
    return json.loads(m_decode)

 
# Connection to the broker
def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        # If connection is connected
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client()
    client.will_set(topic[2][0] , f'{client_id} IS DISCONNECTED', 1 , False)
    # client.username_pw_set(client_id, "123")
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        m_decode=str(msg.payload.decode("utf-8","ignore"))
        print(f"Received `{m_decode}` from `{msg.topic}` topic")
        
        if msg.topic == topic[3][0]: # 5Things/start_traffic
            m_in=string_to_json(m_decode) #decode json data
            
            if m_in["enabled"]:
                start_traffic(m_in)
                print("Traffic Start")
            else:
                traffic_light.clearall()
                traffic_enabled.setTraffic(False)
                traffic_enabled.timer.cancel()
                traffic_enabled.timer.cancel()
                print("Traffic Stop")
                
        else:
            if traffic_enabled.enabled == True:
                m_in=string_to_json(m_decode) #decode json data
                check_traffic_condition(m_in) 
    
   
    
    client.subscribe([topic[1], topic[3]])
    client.on_message = on_message
    

         
def start_time(enabled):
    trafficStatus.change(enabled)
    timer = RepeatTimer(10,normal_traffic,args=[])
    traffic_enabled.setTimer(timer)
    traffic_enabled.timer.start()
    # timer.start
        

        
if __name__ == "__main__":
    try:        
        client = connect_mqtt()
        subscribe(client)
        client.loop_forever()
        
    except KeyboardInterrupt:
        # traffic_light.clearall()
        timer.cancel()
