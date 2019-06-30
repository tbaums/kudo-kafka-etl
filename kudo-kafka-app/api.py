import os
import socket
import logging
import kafka_ingest
import kafka_generator
import ifaddr


from flask import Flask, Response, request, render_template
from flask_api import status
from kafka import KafkaConsumer


app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
app.logger.addHandler(logging.StreamHandler())
app.logger.setLevel(logging.INFO)

###########################
# Remote Control Interface 
###########################

@app.route('/rc')
def rcUI():
    return render_template('rc.html')


###########################
# Set color
###########################

@app.route('/set-color/<color>')
def set_color(color):
    x = kafka_generator.send_message({"topic": "color","value": color})
    return Response(str(x), mimetype='text/plain')

@app.route('/get-color')
def get_color():
    result = kafka_ingest.get_messages("color")

    return Response(str(result), mimetype='text/plain')


## Live updates a list of Numbers being read from a kafka topic called "numbers"

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