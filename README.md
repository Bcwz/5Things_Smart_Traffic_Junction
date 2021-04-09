# 5Things_Smart_Traffic_Junction

## Files

### MQTT_Broker.py
The broker have to be setup first in order for other client to connect

![image](https://user-images.githubusercontent.com/16936739/114174886-dfc96400-996b-11eb-87d6-248999a0e25e.png)

Change the broker ip address to the local computer ip address

### MQTT_Nano.py
The nano acted as a traffic controller. It will configure what is needed to run at the application

![image](https://user-images.githubusercontent.com/16936739/114175005-0f786c00-996c-11eb-9d6d-f9d13aa37c25.png)

Change the IP address to the broker ip address

### MQTT_Traffic.py
This is to be put at the Raspberry PI.

![image](https://user-images.githubusercontent.com/16936739/114175005-0f786c00-996c-11eb-9d6d-f9d13aa37c25.png)

Change the IP address to the broker ip address

### IOT_Color.py
This is to be put at the Raspberry PI for the sense hat to change its color

![image](https://user-images.githubusercontent.com/16936739/114175005-0f786c00-996c-11eb-9d6d-f9d13aa37c25.png)

Change the IP address to the broker ip address

### Camera.py
This can be run either at the raspberry or local computer. This file is able to run the scenerio to change the traffic status

![image](https://user-images.githubusercontent.com/16936739/114175005-0f786c00-996c-11eb-9d6d-f9d13aa37c25.png)

Change the IP address to the broker ip address


1) Run the MQTT_Broker.py
2) Run any file for client to connect to the broker
3) Run the Camera.py and enter any of the number to see the changes!

