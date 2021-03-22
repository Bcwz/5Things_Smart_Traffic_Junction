import logging
import asyncio
from hbmqtt.broker import Broker



logger = logging.getLogger(__name__)

config = {
    'listeners': {
        'default': {
            'type': 'tcp',
            'bind': '192.168.1.85:1883'    # 0.0.0.0:1883
        }
    },
    'sys_interval': 10,
    'topic-check': {
        'enabled': True,
        'plugins': ['topic_taboo'],
    }
}

broker = Broker(config)


async def startBroker():
    await broker.start()



if __name__ == '__main__':
    formatter = "[%(asctime)s] :: %(levelname)s :: %(name)s :: %(message)s"
    logging.basicConfig(level=logging.INFO, format=formatter)
    asyncio.get_event_loop().run_until_complete(startBroker())

    asyncio.get_event_loop().run_forever()
