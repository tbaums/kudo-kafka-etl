# Before running this program run pip install kafka-python
import datetime
import os, sys

from kafka import KafkaConsumer
from json import loads

print("App started X")



def get_consumer(topic):
    consumer = KafkaConsumer(
        'demo-transactions',
        bootstrap_servers=[os.environ['BROKER_SERVICE']],
        auto_offset_reset='earliest',
        consumer_timeout_ms=1000)

    consumer.subscribe([str(topic)])
    return consumer


def get_messages(topic):
    print("E")
    messages = []
    consumer = get_consumer(str(topic))


    for message in consumer:
        messages.append(str(message))
    consumer.close()
    return messages
