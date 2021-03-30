from threading import Thread
import time
import random
from threading import Timer



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

        
    
        
# def red_light_time():
#     colour = "RED"
#     print(colour)
#     CURRENT_COLOUR = colour
#     for i in range(5, 0, -1):
#         time.sleep(1)
#         TIME_LEFT = i
#         print(f'red + {i}')  # this i to pass to check time left
        
        
# # green light time
# def green_light_time():
#     colour = "Green"
#     print(colour)
#     CURRENT_COLOUR = colour
#     for i in range(5, 0, -1):
#         time.sleep(1)
#         TIME_LEFT = i
#         print(f'green + {i}')  # this i to pass to check time left

def car_count(roadStatus):
    # If a car reach the length of 7, inform the traffic to change the light at the controller
    # while True:
    count = random.randint(0, 7)
    roadStatus.setRoadCount(count)
    
def emergency_bool(roadStatus):
    # If a car reach the length of 7, inform the traffic to change the light at the controller
    # while True:
    count = random.randint(0,2)
    if count == 0:
        roadStatus.setRoadEmegency(True)

def check_traffic_condition(roadStatus):
    # while True:
    if roadStatus.numOfCar == 7 or roadStatus.emergency is True:
        print(roadStatus.numOfCar)
        print(roadStatus.emergency)
        timer.cancel()
 
        
def transit_green_to_red():
    print("Amber")
    time.sleep(3)
    print("Red")


def transit_red_to_green():
    print("Traffic is now Green")



def normal_traffic(trafficStatus):
    # If this is traffic turn to green
    if trafficStatus.status is True:
        transit_red_to_green()
        
        # Traffic prepare to change to red after the next timing
        trafficStatus.change(False)
        # transit_red_to_green()
    else:
        transit_green_to_red()
        trafficStatus.change(True)


    # end the time when the script finish
    # finish = time.perf_counter()

    # print(f"time taken to finish thread: {finish-start}")
        
if __name__ == "__main__":
    try:
        tStatus = TrafficStatus(True)
        print("Red")
        timer = RepeatTimer(3,normal_traffic,args=[tStatus])
        timer.start()
        
        while True:
            roadStatus = RoadCar()

            car_count(roadStatus)
            emergency_bool(roadStatus)
            check_traffic_condition(roadStatus) 
            time.sleep(3)
        
    except KeyboardInterrupt:
        timer.cancel()
    # t1 = Thread(target = normal_traffic, daemon=True)
    # t2 = Thread(target = check_traffic_condition, daemon=True)
    
    # t1.start()
    # t2.start()
