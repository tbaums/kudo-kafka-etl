# Before running this program run pip install kafka-python
import datetime
import os, sys
import time
import logging

from kafka import KafkaProducer
from json import loads, dumps


print("App started X")

# try:
#     messages 
# except NameError:
#     messages = []



def get_producer():
    try:
        # producer = KafkaProducer(
        #                         bootstrap_servers=[os.environ['BROKER_SERVICE']]
        #                         # , wakeup_timeout_ms=30000
        #                         , request_timeout_ms=60000
        #                         )
        producer = KafkaProducer(bootstrap_servers=[os.environ['BROKER_SERVICE']]
                                , value_serializer=lambda x: dumps(x).encode('utf-8')
                                , acks=1
                                # , max_in_flight_requests_per_connection=1
                                , retries=1
                                # , batch_size=0
                                )
        return producer
    except:
        logging.warning("could not connect to Kafka")

def send_message(message):
    producer = get_producer()
    # return [message["topic"], message["value"]]
    msg_json = {'color': message["value"]}
    producer.send(message["topic"], value=msg_json)
    producer.close()
    return [message["topic"], msg_json]

def send_messages(topic):
    # try:
    #     producer = get_producer()
    #     for e in range(1000):
    #         logging.debug("Sending number: \n")
    #         logging.debug(e)
    #         logging.debug("\n ********************* \n")
    #         # data = {'number' : e}
    #         logging.debug("Data JSON: %s" % data)
    #         # producer.send(topic, value=data)
    #         producer.send('numbers', b'1')
    #         producer.flush()
    #     return 
    # except:
    #     return "There was an error"
    producer = get_producer()
    for e in range(1000):
        data = {'number' : e}
        producer.send(topic, value=data)
        # producer.flush()
        # sleep(5)
    producer.close()
    return 