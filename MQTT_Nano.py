# publisher
from paho.mqtt import client as mqtt_client
import json

# broker = '172.30.138.214'
broker = '192.168.1.85'
port = 1883

# # TODO Chnage the traffic light
topic = [("5Things/traffic_change",2), ("5Things/traffic_condition",2), ("5Things/start_stop",2), ("5Things/set_traffic", 2)]

# # generate client ID with pub prefix randomly
client_id = "traffic_controller"

# The fixed timing for time extension
TIME_EXTENSION = 10



# Connection to the broker
def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        # If connection is connected
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client()
    # client.username_pw_set(client_id, "123")
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

def publish(client, message, topic):
    msg_count = 0
    # Return the number of car being generated
    msg = f'{message}'
    
    
    # Publis the message
    result = client.publish(topic, msg, 2)
 
    
    print(f"Send `{msg}` to topic `{topic}`")
   

def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        m_decode=str(msg.payload.decode("utf-8","ignore"))
        payload = m_decode 

        print(f"Received `{m_decode}` from `{msg.topic}` topic")
        
        if msg.topic == topic[0][0]:
            decode_payload = string_to_json(m_decode) #decode json data
            payload = traffic_condition(decode_payload)
            setTopic = topic[1][0]
        else:
            setTopic = topic[3][0]
            
            
        publish(client, payload, setTopic)
        
    client.subscribe([topic[0],topic[2]])
    client.on_message = on_message

def traffic_condition(traffic):
    # If the traffic light timer still green
    if traffic['enabled']:
        message = f'{{"direction" : "{traffic["direction"]}", "time_extended": {TIME_EXTENSION}}}'
    
    return message

def string_to_json(m_decode):
    return json.loads(m_decode)

def json_to_string(m_decode):
    return json.dumps(m_decode)
    
client = connect_mqtt()
subscribe(client)
client.loop_forever()