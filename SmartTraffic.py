import multiprocessing as mp
import time


# start the time when the script runs
start = time.perf_counter()
 
def test():
    print("im test")
    time.sleep(5)
    print("im tested")

def sest(event):
    print("im sest")
    a=5
    if a == 5:
        event.set()
        #print("killing p1...")
        #process.terminate()
        time.sleep(20)
    print("done terminating p1")

if __name__ == '__main__':
    # create event
    event = mp.Event()
    
    p1 = mp.Process(target=test)
    p2 = mp.Process(target=sest, args=(event,))

    p1.start()
    p2.start()

    # check if event is set
    while True:
        if event.is_set():
            print("killing p1...")
            p1.terminate()
            break
       

    p1.join()
    p2.join()
    '''
    for i in range(5,0,-1):
        time.sleep(1)
        print(i)
    '''

    # end the time when the script finish
    finish = time.perf_counter()

    print(f"time taken to finish thread: {finish-start}")