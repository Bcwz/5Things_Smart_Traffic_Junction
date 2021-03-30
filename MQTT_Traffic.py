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

broker = '172.30.138.214'
port = 1883


FLAG_SMART_TRAFFIC = 0
ENABLE_SMART_TRAFFIC = 1
DISABLE_SMART_TRAFFIC = 2

# # TODO Chnage the traffic light
topic = [("5Things/traffic_change",2), ("5Things/traffic_condition",2), ("5Things/start_stop",2), ("5Things/set_traffic", 2)]

# # generate client ID with pub prefix randomly
client_id = "east"
# client_id = "north"
traffic_lookout = ["west", "east"]
# traffic_lookout = ["north", "south"]

now = datetime.datetime.now()
# dd/mm/YY H:M:S
dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

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
        
class EnableTraffic:
    def __init__(self, enabled = False, timer = None):
        self.enabled = enabled
        self.timer = timer
    
    def setTimer(self, timer):
        self.timer = timer
        
    def setTraffic(self, enabled):
        self.enabled = enabled
            

sTraffic = SmartTraffic(FLAG_SMART_TRAFFIC, 0)
traffic_enabled = EnableTraffic()


def check_traffic_condition(status):
    # while True:
    sTraffic.setSmartTraffic(DISABLE_SMART_TRAFFIC)
    if status["direction"] in traffic_lookout:
        sTraffic.setSmartTraffic(ENABLE_SMART_TRAFFIC)
    sTraffic.setTimeExtended(status["time_extended"] + sTraffic.time_extended)
 
        
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

def reset():
    sTraffic.setSmartTraffic(FLAG_SMART_TRAFFIC)
    sTraffic.setTimeExtended(0)

def normal_traffic(trafficStatus): 
   
    print("Start =", dt_string)

    if sTraffic.enabled is not FLAG_SMART_TRAFFIC:
  
        if sTraffic.enabled == ENABLE_SMART_TRAFFIC and trafficStatus.status is True:
            extend_smart_traffic()
            
        elif sTraffic.enabled == DISABLE_SMART_TRAFFIC and trafficStatus.status is False:
            extend_smart_traffic()
        
        elif sTraffic.enabled == ENABLE_SMART_TRAFFIC and trafficStatus.status is False:
            traffic_light.blue()
            trafficStatus.change(False)
        
        elif sTraffic.enabled == DISABLE_SMART_TRAFFIC and trafficStatus.status is True:
            traffic_light.blue()
            trafficStatus.change(True)
        
        reset()

    # If this is traffic turn to green
    if trafficStatus.status is True:
        transit_red_to_green()
        trafficStatus.change(False)
        
        # if sTraffic.enabled is True:
            # run_smart_traffic()
        #     print(sTraffic.enabled)
        #     # print("Smart Traffic Enabled")
        #     time.sleep(sTraffic.time_extended)
        #     reset()
        #     # print("Smart Traffic Disabled")

        
    else:
        transit_green_to_red()
        trafficStatus.change(True)
        
        # if sTraffic.enabled is False:
        #     run_smart_traffic()
        #     print(sTraffic.enabled)
        #     # print("Smart Traffic Enabled")
        #     time.sleep(sTraffic.time_extended)
        #     reset()
        #     # print("Smart Traffic Disabled")
        

        
    
    print("End =", dt_string)	

def extend_smart_traffic():
    traffic_light.blue()
            # print("Smart Traffic Enabled")
    time.sleep(sTraffic.time_extended)
    
    if sTraffic.enabled is True:
        sTraffic.setSmartTraffic(FLAG_SMART_TRAFFIC)
        run_smart_traffic()
    
    else:
        reset()
    
    

 
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
        
        if msg.topic == topic[3][0]: # 5Things/start_traffic
            m_in=string_to_json(m_decode) #decode json data
            
            if m_in["enabled"]:
                start_traffic(m_in)
                print("Traffic Start")
            else:
                traffic_light.clearall()
                traffic_enabled.setTraffic(False)
                traffic_enabled.timer.cancel()
                print("Traffic Stop")
                
        else:
            if traffic_enabled.enabled == True:
                m_in=string_to_json(m_decode) #decode json data
                check_traffic_condition(m_in) 
    
   
    
    client.subscribe([topic[1], topic[3]])
    client.on_message = on_message
    
    
def string_to_json(m_decode):
    return json.loads(m_decode)

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
         
def start_time(enabled):
    tStatus = TrafficStatus(enabled)
    timer = RepeatTimer(10,normal_traffic,args=[tStatus])
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
