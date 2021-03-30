import time
from tb_device_mqtt import TBDeviceMqttClient, TBPublishInfo

telemetry = {"Attribute": 41.9, "enabled": False, "Gideon Status": "Yesn't"}

# Timer start counting from connecting 
start_time = time.time()
#Please dont change this IP address and Token
client = TBDeviceMqttClient("129.126.163.157", "TrafficController")

client.connect()
client.send_telemetry(telemetry) 
result = client.send_telemetry(telemetry)
success = result.get() == TBPublishInfo.TB_ERR_SUCCESS

client.disconnect()
print("--- %s seconds ---" % (time.time() - start_time))