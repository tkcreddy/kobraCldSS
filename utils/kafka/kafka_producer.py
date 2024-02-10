import asyncio
from aiokafka import AIOKafkaProducer
from utils.ReadConfig import ReadConfig as rc
class AsyncKafkaProducerWithState:
    def __init__(self, bootstrap_servers, topic):
        self.bootstrap_servers = bootstrap_servers
        self.topic = topic
        print(bootstrap_servers)
        self.producer = AIOKafkaProducer(bootstrap_servers=bootstrap_servers)
        self.state = {}

    async def produce_message(self, message):
        await self.producer.start()

        # Produce a message to the specified topic
        await self.producer.send_and_wait(self.topic, message.encode('utf-8'))

        # Update state (for example, track the last produced message offset)
        metadata = await self.producer.get_metadata(self.topic)
        partitions = metadata.topics[self.topic].partitions
        for partition in partitions:
            self.state[partition.id] = partition.leader.highwater

        await self.producer.stop()
read_config = rc('/Users/krishnareddy/PycharmProjects/kobraCld/config/config.json')
kafka_config = read_config.kafka_config
print(kafka_config['bootstrap_servers'])
# Example usage
bootstrap_servers = kafka_config['bootstrap_servers']
topic = kafka_config['topic']
producer = AsyncKafkaProducerWithState(bootstrap_servers,topic)
asyncio.run(producer.produce_message('Hello, Kafka!'))
print("Producer state:", producer.state)
