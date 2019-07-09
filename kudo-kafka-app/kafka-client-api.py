import os, sys
import socket
import logging
import time
import random
import json
import urllib

from flask import (
    Flask,
    Response,
    request,
    render_template,
    jsonify,
    stream_with_context,
    json,
)
from kafka import KafkaConsumer, KafkaProducer

if sys.version_info[0] == 3:
    os.environ["PYTHONUNBUFFERED"] = "1"


logging.basicConfig(level=logging.INFO)
app = Flask(__name__)


###################################
#              API                #
###################################

# This API is designed to be extremely simple, testable, and extensible by the widest possible audience.
#
# The API contains only two methods, `read` and `write`.


# WRITE_TO_KAFKA ----------------------------------------------
# write (topic: <string>, payload: <JSON object>, repetitions: <int>)
# The `repetitions` parameter indicates the number of times you want the message written to Kafka.
# This allows simulation of high load write behavior to Kafka.

# WARNING: 
# Due to the highly janky nature of this implementation, you CANNOT write any "," characters 
# to Kafka, or the message will not be readable by READ_FROM_KAFKA.


# READ_FROM_KAFKA ----------------------------------------------
# read (topic: <string>, group_id: <string>)


# NOTE: The route below assumes that Ingress provided at /kafka-client-api.
# If you change this Ingress path to something else, you must change the routing below.
@app.route("/kafka-client-api/write", methods=["POST"])
def write():
    query_string = urllib.parse.parse_qs(request.query_string.decode("UTF-8"))
    app.logger.info("Request query_string: " + str(query_string))
    topic = query_string["topic"][0]
    payload = query_string["payload"][0]
    repetitions = int(query_string["repetitions"][0])

    write_to_kafka(topic, payload, repetitions)
    return Response("WRITE REQUEST RECEIVED", mimetype="text/plain")


@app.route("/kafka-client-api/read", methods=["GET"])
def read():
    query_string = urllib.parse.parse_qs(request.query_string.decode("UTF-8"))
    app.logger.info("Request query_string: " + str(query_string))
    topic = query_string["topic"][0]
    group_id = query_string["group_id"][0]

    read_from_kafka(topic, group_id)
    return Response("READ REQUEST RECEIVED", mimetype="text/plain")


###################################
#      KAFKA PRODUCER CLIENT      #
###################################
def get_producer():
    try:
        producer_client = KafkaProducer(
            bootstrap_servers=[os.environ["BROKER_SERVICE"]],
            value_serializer=lambda x: json.dumps(x).encode("utf-8"),
            acks=1,
        )
    except Exception as e:
        app.logger.error("Could not create producer_client with error " + str(e))
    return producer_client


def write_to_kafka(topic, payload, repetitions):
    producer_client = get_producer()
    for _ in range(repetitions):
        try:
            producer_client.send(topic, payload)
            # producer_client.send(topic, value="test")
            app.logger.info(
                "Sent to Kafka. Topic: " + topic + " Value: " + str(payload)
            )

        except Exception as e:
            app.logger.error(
                "could not send message to " + topic + " with payload " + str(payload)
            )
            app.logger.error("send message failed with error: " + str(e))
    producer_client.close()
    return


###################################
#      KAFKA CONSUMER CLIENT      #
###################################


def get_consumer(topic, group_id):
    try:
        consumer = KafkaConsumer(
            topic,
            bootstrap_servers=[os.environ["BROKER_SERVICE"]],
            auto_offset_reset="earliest",
            enable_auto_commit=True,
            group_id=str(group_id)
        )
        return consumer
    except Exception as e:
        return "failed to connect KafkaConsumer with error: " + str(e)


def read_from_kafka(topic, group_id):
    try:
        consumer_client = get_consumer(topic, group_id)
    except Exception as e:
        app.logger.error("Could not create consumer_client with error " + str(e))

    messages = []
    for message in consumer_client:
        # app.logger.info(str(json.dumps(message)))
        # msg = json.loads(json.dumps(str(message)))
        # trim off "ConsumerRecord(" string from beggining of message and ")" from end.
        # trimmed_msg = msg[15 : len(msg) - 2]
        # payload = msg.split(",")

        app.logger.info(json.loads(message.value))
    consumer_client.close()


###################################
#             RUN                 #
###################################
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=float(os.getenv("DW_PORT", "8080")))

