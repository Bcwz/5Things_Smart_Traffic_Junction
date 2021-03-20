import threading
import time
import logging

# Do a thread to receiving the information of what is being return
# Without affecting the main program.
def publoish_function(name):
    time.sleep(2)
    

def normal_traffic():
    print("Green")
    print("Yellow")
    print("Red")
    


if __name__ == "__main__":
    publish = threading.Thread(target=thread_function, args=(1,))
    publish.start()
    