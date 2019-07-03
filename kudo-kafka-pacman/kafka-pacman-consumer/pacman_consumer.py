import datetime
import os, sys
import socket
import time
import logging
import datetime
from json import loads, dumps
import random

from kafka import KafkaConsumer
from kafka.admin import KafkaAdminClient

# ***********
#  Globals  #
# ***********
start_time = ""


def get_host_name():
    return socket.gethostname()[-6:-1]


def get_consumer():
    consumer = KafkaConsumer(
        bootstrap_servers=os.environ["BROKER_SERVICE"],
        group_id="pacman-consumers-group",
        value_deserializer=lambda v: loads(v.decode("utf-8")),
    )
    consumer.subscribe([os.environ["PACMAN_JOBS_TOPIC"]])
    return consumer


def get_current_time():
    return datetime.datetime.now()


def set_start_time():
    global start_time
    start_time = get_current_time()
    return start_time


def get_start_time():
    return start_time


if __name__ == "__main__":
    while True:
        if "consumer" not in locals():
            consumer = get_consumer()
            print(get_host_name(), "----got consumer:", consumer)
        msgs_processed_this_connection = 0
        proc_start_time = set_start_time()
        for msg in consumer:
            msgs_processed_this_connection += 1

            if msgs_processed_this_connection % 10000 == 0:
                processing_time = get_current_time() - get_start_time()
                msgs_processed_per_second = str(round(msgs_processed_this_connection / float(processing_time.seconds + processing_time.microseconds / 1000000)))
                sys.stdout.write(
                    str(
                        {
                            "messages_processed_this_connection": msgs_processed_this_connection,
                            "processing_time": str(processing_time),
                            "messages_processed_per_second": msgs_processed_per_second
                        }
                    )
                )

