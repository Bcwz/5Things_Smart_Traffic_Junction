from sense_hat import SenseHat
from time import sleep

sense = SenseHat()

def red(): 
    red = (255,0,0)
    sense.clear(red)
    sleep(1)
    sense.clear()

def green(): 
    green = (0,255,0)
    sense.clear(green)
    sleep(1)
    sense.clear()

def orange(): 
    orange = (255,165,0)
    sense.clear(orange)
    sleep(1)
    sense.clear()
   
    
    

if __name__ == '__main__':
    orange()
    red()
    green()