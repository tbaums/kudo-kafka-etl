import datetime
import os, sys
import socket
import time
import logging
from json import loads, dumps
import random

from kafka import KafkaProducer
from kafka.admin import KafkaAdminClient, NewTopic

logging.basicConfig()

def log(content):
    sys.stdout.write(str(content))

def get_admin_client():
    try:
        admin_client = KafkaAdminClient(bootstrap_serviers=os.environ['BROKER_SERVICE'])
        return admin_client
    except Exception as e:
        log(e)



def create_topic_obj(topic_name=[os.environ["PACMAN_JOBS_TOPIC"]], partitions=10):
    new_topic = NewTopic(topic_name, num_partitions=partitions, replication_factor=1)
    return new_topic

def create_new_topic(topic_obj):
    admin_client = get_admin_client()
    try:
        admin_client.create_topics([topic_obj])
    except Exception as e:
        log(e)

def get_producer():
    producer = KafkaProducer(
        bootstrap_servers=[os.environ["BROKER_SERVICE"]],
        value_serializer=lambda v: dumps(v).encode("utf-8")
    )
    return producer


def send_message(producer, json):
    return producer.send(os.environ["PACMAN_JOBS_TOPIC"], json)


if __name__ == '__main__':
    try:
        create_new_topic(create_topic_obj()) 
        log('created new topic')
    except Exception as e:
        log('failed to create NewTopic w/exception: ', e )
        sys.exit()

    producer = get_producer()
    msgs_sent_counter = 0
    while True:
        
        json = {'number': str(random.randint(1,1000)), 'text': 'This is some message text...' * random.randint(1,10)}
        result = send_message(producer or get_producer(), json)
        # print(int(json['number']), ',')
        
        msgs_sent_counter += 1
        if (msgs_sent_counter % 10000 == 0):
            log_string = '-----Msgs sent: ' + str(msgs_sent_counter) + ' to topic ' + os.environ["PACMAN_JOBS_TOPIC"]
            log(log_string)
        time.sleep(.000000000001)