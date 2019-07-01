import os
import socket
import logging
import kafka_ingest
import kafka_generator
import ifaddr
import time
import random


from flask import Flask, Response, request, render_template, jsonify, stream_with_context, json
from flask_api import status
from kafka import KafkaConsumer


app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
app.logger.addHandler(logging.StreamHandler())
app.logger.setLevel(logging.INFO)

###########################
# Remote Control Interface
###########################

@app.route('/v0alpha1/rc')
def rcUI():
    return render_template('rc.html')

###########################
# Set color
###########################

@app.route('/v0alpha1/generate-stocks-stream')
def generate_ticker_stream():
    for _ in range(10000):
        x = kafka_generator.send_message({"topic" : "stocks", "value": {"name": "GE", "value": random.randint(1,99)}})
    return Response(str(x), mimetype='text/plain')

@app.route('/v0alpha1/get-stocks-stream')
def get_stocks_stream():
    def f():
        try:
            consumer = kafka_ingest.get_consumer(10000, 'stocks-group', "stocks")
        except:
            "could not connect to Kafka"
    
        for message in consumer:
            # yield str(json.dumps(message).split(',')[6])
            yield str(json.dumps(message.value["stocks"]))
            # yield str(json.dumps(message).split(',')[6])
        consumer.commit()
        consumer.close()
    return Response(stream_with_context(f()), mimetype="text/event-stream")




###########################
# Set color
###########################

@app.route('/v0alpha1/set-color/<color>')
def set_color(color):
    x = kafka_generator.send_message({"topic": "color","value": color})
    return Response(str(x), mimetype='text/plain')

@app.route('/get-color')
def get_color():
    consumer = kafka_ingest.get_consumer(200, "color")

    messages = []
    for message in consumer:
        messages.append(message)
    consumer.commit()
    consumer.close()    

    return Response(str(messages), mimetype='text/plain')


@app.route('/v0alpha1/get-color')
def stream():
    def f():
        try:
            consumer = kafka_ingest.get_consumer(500, 'color-group',"color")
        except:
            "could not connect to Kafka"
    
        for message in consumer:
            yield str(json.dumps(message).split(',')[6])
        consumer.commit()
        consumer.close()
    return Response(stream_with_context(f()), mimetype="text/event-stream")


########################################################################################    
## Live updates a list of Numbers being read from a kafka topic called "numbers"
########################################################################################

@app.route('/numbers')
def numbers():
    logging.debug("got here \n Result is: \n ************************ \n")
    result = kafka_ingest.get_messages("numbers")
    logging.debug(result)
    return Response(str(result), mimetype='text/plain')
    # return Response("OK", mimetype='text/plain')

@app.route('/')
@app.route('/numbers-ui')
def numbersConsumer():
    # result = " "
    return render_template('home.html', messages_endpoint="/numbers")

@app.route('/generate-numbers')
def generateNumbers():
    kafka_generator.send_messages("numbers")
    return Response("OK", mimetype='text/plain')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=float(os.getenv('DW_PORT', '80')))