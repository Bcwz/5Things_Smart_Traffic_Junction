import logging
import asyncio
from hbmqtt.broker import Broker
from hbmqtt.client import MQTTClient, ClientException


logger = logging.getLogger(__name__)

topic = [("5Things/traffic_change",2), ("5Things/traffic_condition",2), ("5Things/start_stop",2), ("5Things/set_traffic", 2)]

config = {
    'listeners': {
        'default': {
            'type': 'tcp',
            'bind': '192.168.1.85:1883'    # 0.0.0.0:1883
        }
    },
    'sys_interval': 10,
    # 'auth': {
    #     'plugins' : ['auth.anonymous'], #List of plugins to activate for authentication among all registered plugins
    #     'allow-anonymous': False,
    #     'password-file': 'password.txt'
    # }, 
    'topic-check': {
        'enabled': True,
        'plugins': ['topic_taboo']
        # 'plugins': ['topic_taboo','topic_acl'],
        # 'acl':{
        #     'traffic_controller': ['5Things/#'],
        #     'traffic_north': ['5Things/#'],
        # }
    }, 
}


broker = Broker(config)


async def startBroker():
    await broker.start()



async def brokerGetMessage():
    C = MQTTClient()
    await C.connect('mqtt://192.168.1.85:1883/')
    await C.subscribe([topic[2]])

    logger.info('Subscribed!')
    try:
        for i in range(1,100):
            message = await C.deliver_message()
            packet = message.publish_packet
            print(packet.payload.data.decode('utf-8'))
    except ClientException as ce:
        logger.error("Client exception : %s" % ce)

if __name__ == '__main__':
    formatter = "[%(asctime)s] :: %(levelname)s :: %(name)s :: %(message)s"
    logging.basicConfig(level=logging.INFO, format=formatter)
    asyncio.get_event_loop().run_until_complete(startBroker())
    asyncio.get_event_loop().run_until_complete(brokerGetMessage())
    asyncio.get_event_loop().run_forever()