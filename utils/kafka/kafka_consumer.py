import asyncio
import json
import time
from aiokafka import AIOKafkaProducer, AIOKafkaConsumer
from utils.ReadConfig import ReadConfig as rc

class AsyncKafkaConsumer:
    def __init__(self, bootstrap_servers, group_id, topic):
        self.bootstrap_servers = bootstrap_servers
        self.group_id = group_id
        self.topic = topic
        self.consumer = AIOKafkaConsumer(
            self.topic,
            bootstrap_servers=bootstrap_servers,
            group_id=group_id,
            auto_offset_reset='earliest',  # You can change this to 'latest' if you want to start from the latest offset
            enable_auto_commit=True,
        )
        self.state = {}

    async def consume_messages(self):
        await self.consumer.start()
        msg_json=''
        # Consume messages
        try:
            async for msg in self.consumer:
                # Process the received message
                #print('Received message: {}'.format(msg.value.decode('utf-8')))
                #print(msg.value.decode('utf-8'))
                msg_json=msg.value.decode('utf-8')
                print(msg_json)

                # Update state (for example, track the last consumed message offset)
                self.state[msg.partition] = msg.offset
        finally:
            await self.consumer.stop()
        return msg_json

async def main():
    read_config = rc('/Users/krishnareddy/PycharmProjects/kobraCld/config/config.json')
    kafka_config = read_config.kafka_config
    print(kafka_config['bootstrap_servers'])
    #producer = AsyncKafkaProducerWithState(kafka_config['bootstrap_servers'], kafka_config['topic'])
    consumer = AsyncKafkaConsumer(kafka_config['bootstrap_servers'], kafka_config['group_id'], kafka_config['topic'])
    #msg_id=0
    #async consumer.consume_messages()
    msg_json=''
    await consumer.consumer.start()
    async for  msg in consumer.consumer:
        msg_json=msg.value.decode('utf-8')
    await consumer.consumer.stop()
    print(msg_json)


if __name__ == "__main__":
    asyncio.run(main())
