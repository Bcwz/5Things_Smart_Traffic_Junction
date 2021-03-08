from sense_hat import SenseHat
from time import sleep

red = (255,0,0)
green = (0,255,0)
orange = (255,165,0)

sense = SenseHat()

sense.clear((orange))
sleep(1)
sense.clear()