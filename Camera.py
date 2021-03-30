# publisher
import paho.mqtt.client as mqtt

client_id = "traffic_camera"
client = mqtt.Client(client_id)

# Set IP address
client_ip = "172.30.138.214"

client.connect(client_ip, 1883)
# client.username_pw_set(client_id)

while True:
    result = input("Please select from: \n [1] Traffic Vertical Reach 7 car \n [2] Traffic Vertical Emergency \n [3] Traffic Horizontal Reach 7 car \n [4] Traffic Vertical Emergency \n Choose your input: ")
    
    if int(result) == 1:
        payload = f'{{ "enabled": true, "direction":"north" }}'
        client.publish("5Things/traffic_change", payload)
        
    elif int(result) == 2:
        payload = f'{{ "enabled": true, "direction":"north" }}'
        client.publish("5Things/traffic_change", payload)
        
    elif int(result) == 3:
        payload = f'{{ "enabled": true, "direction":"west" }}'
        client.publish("5Things/traffic_change", payload)
        
    elif int(result) == 4:
        payload = f'{{ "enabled": true, "direction":"west" }}'
        client.publish("5Things/traffic_change", payload)
    else:
        print("Please choose from 1 to 4\n")
        
    print(f'You have selected {result} \n')
   