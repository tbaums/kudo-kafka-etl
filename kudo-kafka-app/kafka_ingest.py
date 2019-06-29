# Before running this program run pip install kafka-python
import datetime
import os, sys

from kafka import KafkaConsumer
from json import loads

print("App started X")


def get_consumer(topic):

    try:
        consumer = KafkaConsumer(
            topic
            , bootstrap_servers=[os.environ['BROKER_SERVICE']]
            , auto_offset_reset='earliest'
            , enable_auto_commit=True
            , consumer_timeout_ms=5000
            , value_deserializer=lambda x: loads(x.decode('utf-8'))
            , group_id='my-group'
            )
        # sys.stdout.write("got consumer \n")
        # consumer.subscribe([str(topic)])
        # sys.stdout.write("subscribed to topic: \n")
        # sys.stdout.write(topic)
        return consumer
    except:
        return "failed to connect to Kafka"


def get_messages(topic):
    print("E")
    consumer = get_consumer(str(topic))

    messages = []
    for message in consumer:
        # messages.append({str(message.value) : str(message.key)})
        messages.append(message.value)
    consumer.commit()
    consumer.close()
    # print(messages)
    return messages
