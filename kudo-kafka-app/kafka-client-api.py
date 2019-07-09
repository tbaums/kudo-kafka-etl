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
# from kafka import (KafkaConsumer, KafkaProducer)


app = Flask(__name__)
# logging.basicConfig(level=logging.INFO)


###################################
#              API                #
###################################

# This API is designed to be extremely simple, testable, and extensible by the widest possible audience.
#
# The API contains only two methods, `read` and `write`.


# WRITE
# write (topic: <string>, payload: <JSON object>, repititions: <int>)
# The `repititions` parameter indicates the number of times you want the message written to Kafka.
# This allows simulation of high load write behavior to Kafka.




# NOTE: The route below assumes that Ingress provided at /kafka-client-api.
# If you change this Ingress path to something else, you must change the routing below.
@app.route("/kafka-client-api/write", methods=['POST'])
def write():
    query_string = urllib.parse.parse_qs(request.query_string.decode('UTF-8'))
    sys.stdout.write("Request query_string: " + str(query_string))

    return Response("MESSAGE SENT", mimetype="text/plain")


###################################
#      KAFKA PRODUCER CLIENT      #
###################################


###################################
#      KAFKA CONSUMER CLIENT      #
###################################


###################################
#             RUN                 #
###################################
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=float(os.getenv("DW_PORT", "8080")))

