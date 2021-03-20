import logging
import asyncio
from hbmqtt.broker import Broker
from hbmqtt.client import MQTTClient, ClientException
from hbmqtt.mqtt.constants import QOS_1

logger = logging.getLogger(__name__)

config = {
    'listeners': {
        'default': {
            'type': 'tcp',
            'bind': '192.168.1.88:9999'    # 0.0.0.0:1883
        }
    },
    'sys_interval': 10,
    'topic-check': {
        'enabled': False
    }
}

broker = Broker(config)


async def startBroker():
    await broker.start()

@asyncio.coroutine
def brokerGetMessage():
    C = MQTTClient()
    await C.connect('mqtt://192.168.1.88:9999/')
    await C.subscribe([
        ("LINTANGtopic/test", QOS_1)
    ])
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