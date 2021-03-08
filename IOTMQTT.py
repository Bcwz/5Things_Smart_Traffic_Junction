import time
from time import sleep
from sense_hat import SenseHat
import paho.mqtt.client as mqtt #use sudo pip3 install paho-mqtt



def messageFunction (client, userdata, message):

    topic = str(message.topic)

    message = str(message.payload.decode("utf-8"))

    print(topic + message)

 

ourClient = mqtt.Client("makerio_mqtt") # Create a MQTT client object

ourClient.connect("test.mosquitto.org", 1883) # Connect to the test MQTT broker

ourClient.subscribe("AC_unit") # Subscribe to the topic AC_unit

ourClient.on_message = messageFunction # Attach the messageFunction to subscription

ourClient.loop_start() # Start the MQTT client

 

 

# Main program loop

while(1):

    ourClient.publish(" AC_unit ", " on ") # Publish message to MQTT broker

    time.sleep(1) # Sleep for a second