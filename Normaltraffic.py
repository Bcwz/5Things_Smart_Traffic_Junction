import multiprocessing as mp
import threading as t
import random
import time 
import SmartTraffic as ST

TIME_LEFT = 0
CURRENT_COLOUR = "WHITE"

# start the time when the script runs
start = time.perf_counter()

# TODO get the type of car
def car_count():
    # If a car reach the length of 7, inform the traffic to change the light at the controller
    #while True:
    count = random.randint(0, 10)
    return count

# when traffic light change from red to green
def transit_red_to_green():
    print("i am red for 3s")
    time.sleep(3)
    print("TURN GREEN")
    

# green light time
def green_light_time():
    colour = "Green"
    print(colour)
    CURRENT_COLOUR = colour
    for i in range(5,0,-1):
        time.sleep(1)
        TIME_LEFT = i
        print(f'green + {i}') # this i to pass to check time left

# when traffic light change from green to red
def transit_green_to_red():
    print("i am amber for 3s")
    time.sleep(3)
    print("TURN RED")
   
# red light time
def red_light_time():
    colour = "RED"
    print(colour)
    CURRENT_COLOUR = colour
    for i in range(5,0,-1):
        time.sleep(1)
        TIME_LEFT = i
        print(f'red + {i}') # this i to pass to check time left

def check_traffic_condition():
    while True:
        print("start checking traffic condition")
        counter = car_count()
        if counter >= 7:
            print (f'hello + {counter}') 
            print("publish to mqtt, i want to switch traffic")
            break
        else:
            print("i'm less than 7")

# normal traffic timing
def normal_traffic():
    while True:
        print("all traffic light start from red")
        transit_red_to_green()
        green_light_time() #this is the normal green light timing
        print("im not interrupted")
        transit_green_to_red()
        #red_light_time() #this is the normal red light timing
        
        t1 = t.Thread(target=red_light_time)
        t2 = t.Thread(target=check_traffic_condition)

        t1.start()
        t2.start()

        t1.join()
        t2.join()

        # end the time when the script finish
        finish = time.perf_counter()

        print(f"time taken to finish thread: {finish-start}")

def check_enabled_flag(enable_flag):
    # keep process alive to keep checking for enabled flag
    while True:
        # the real implementation keep subscribe message/topic from mqtt
        # if received enabled = true
        # trigger this event
        # For now is hardcode
        ENABLED = True
        if ENABLED:
            enable_flag.set()
        
def normal_traffic_time_left(time_left_event, time_left, colour_of_traffic):
    # keep process alive to keep checking for light colour and time left
    while True:
        # this condition is when traffic light is currently red
        # if time left for current traffic is more than 10s, call smart traffic
        # else it will remain as the normal traffic
        if time_left > 10:
            ST.smart_traffic(colour_of_traffic)
            time_left_event.set()    


if __name__ == "__main__":

    # create an event to set in a process, so as that normal traffic can be terminated 
    # as a process in this main process if this condition is met
    enabled_flag_event = mp.Event()
    
    # create an event to set in a process, so as that normal traffic can be terminated 
    # as a process in this main process if this condition is met
    time_left_event = mp.Event()
    
    # create normal traffic as a process
    p1 = mp.Process(target=normal_traffic)
    # create enabled flag as a process to check the enabled flag constantly when using subscribe
    p2 = mp.Process(target=check_enabled_flag, args=(enabled_flag_event,))
    # create normal traffic as a process to check the time and current colour constantly of the traffic  
    # if wants to trigger smart traffic
    p3 = mp.Process(target=normal_traffic_time_left, args=(time_left_event, TIME_LEFT, CURRENT_COLOUR))

    # start processes
    p1.start()
    p2.start()
    p3.start()

    # join processes to main process
    p1.join()
    p2.join()
    p3.join()

    # to loop all the processes, and make them keep running
    while True: 
        pass


    '''
    t1 = threading.Thread(target=red_light_time)
    t2 = threading.Thread(target=check_traffic_condition)

    t1.start()
    t2.start()

    t1.join()
    t2.join()

    # end the time when the script finish
    finish = time.perf_counter()

    print(f"time taken to finish thread: {finish-start}")

    while True:
        pass

'''