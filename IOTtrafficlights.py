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
<<<<<<< Updated upstream
    sleep(1)
    sense.clear()
=======
    sleep(1)
    sense.clear()
    
#Colour for default timing
def blue(): 
    orange = (0,0,255)
    sense.clear(orange)
    sleep(1)
    sense.clear()
    
def purple(): 
    orange = (160,32,240)
    sense.clear(orange)
    sleep(1)
    sense.clear()
def pink(): 
    orange = (255,192,203)
    sense.clear(orange)
    sleep(1)
    sense.clear()
    
>>>>>>> Stashed changes
   
    
    

if __name__ == '__main__':
    orange()
    red()
    green()