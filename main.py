# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import asyncio
import argparse
from utils.kafka.producer_kafka import Producer
from utils.ReadConfig import ReadConfig as rc
from utils.CommandConfig import CommandConfig as cc
from utils.server_side.SsOsSystemCmd import SsOsSystemCmd as ss
#from utils.kafka.consumer_kafka import AsyncKafkaConsumer
from logpkg.log_kcld import LogKCld,log_to_file
logger=LogKCld()


@log_to_file(logger)
async def main() ->None:
    parser = argparse.ArgumentParser(description='A Python CLI application')
    parser.add_argument('--configDir', type=str, help='Please specify ConfigDir')
    args = parser.parse_args()
    read_config = rc(args.configDir)
    kafka_config = read_config.kakfa_config
    #os_system_cmd=command_config.os_system_cmd
    os_system_cmd=ss()
    #print(kafka_config['bootstrap_servers'])

    # This is producer from server side sending  the  client to run a  command and return the results
    #Producer sends to Host_topic(topic) for now
    producer=Producer(kafka_config['bootstrap_servers'],kafka_config['topic'])

    # This is consumer that  receives the command output from the client.
    #consumer = AsyncKafkaConsumer(kafka_config['bootstrap_servers'], kafka_config['group_id'], kafka_config['command_output_topic'])
    #print(system_config_info)
    data=os_system_cmd.get_system_info()
    producer.send(data)
    #await consumer.consume_messages()






if __name__ == '__main__':
    asyncio.run(main())
