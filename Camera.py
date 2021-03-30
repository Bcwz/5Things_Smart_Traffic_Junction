# publisher
import paho.mqtt.client as mqtt

client_id = "traffic_camera"
client = mqtt.Client(client_id)

# Set IP address
client_ip = "172.30.138.214"

client.connect(client_ip, 1883)
# client.username_pw_set(client_id)

topic = [("5Things/traffic_change",2), ("5Things/traffic_condition",2), ("5Things/start_stop",2), ("5Things/set_traffic", 2)]

while True:
    result = input("Please select from: \n [1] Traffic North Reach 7 car \n [2] Traffic North Emergency \n [3] Traffic West Reach 7 car \n [4] Traffic West Emergency \n [5] Start West Traffic \n [6] Start North Traffic \n [7] Stop Traffic \n Choose your input: ")
    
    if int(result) == 1:
        payload = f'{{ "enabled": true, "direction":"north" }}'
        client.publish(topic[0][0], payload)
        
    elif int(result) == 2:
        payload = f'{{ "enabled": true, "direction":"north" }}'
        client.publish(topic[0][0], payload)
        
    elif int(result) == 3:
        payload = f'{{ "enabled": true, "direction":"west" }}'
        client.publish(topic[0][0], payload)
        
    elif int(result) == 4:
        payload = f'{{ "enabled": true, "direction":"west" }}'
        client.publish(topic[0][0], payload)
        
    elif int(result) == 5:
        payload = f'{{ "enabled": true, "direction":"west" }}'
        client.publish(topic[2][0], payload)
    
    elif int(result) == 6:
        payload = f'{{ "enabled": true, "direction":"north" }}'
        client.publish(topic[2][0], payload)
        
    elif int(result) == 7:
        payload = f'{{ "enabled": false, "direction":"west" }}'
        client.publish(topic[2][0], payload)
    else:
        print("Please choose from 1 to 4\n")
        
    print(f'You have selected {result} \n')
   