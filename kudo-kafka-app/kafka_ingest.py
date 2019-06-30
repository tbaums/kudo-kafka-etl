# Before running this program run pip install kafka-python
import datetime
import os, sys
from flask import current_app
from kafka import KafkaConsumer
from json import loads



print("App started X")


def get_consumer(topic):

    try:
        # current_app.debug("Getting consumer ***************************************")
        consumer = KafkaConsumer(
            topic
            , bootstrap_servers=[os.environ['BROKER_SERVICE']]
            , auto_offset_reset='earliest'
            , enable_auto_commit=True
            , consumer_timeout_ms=5000
            , value_deserializer=lambda x: loads(x.decode('ascii'))
            , group_id='my-group'
            )
        # current_app.debug("Got consumer ***************************************")
        
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
        print(str(message))
        # current_app.debug(str(message))
        # messages.append({str(message.value) : str(message.key)})
        messages.append(message.value['color'])
    consumer.commit()
    consumer.close()
    # sys.stdout.write(str(messages))
    return messages
