FROM python:alpine
WORKDIR /usr/src/app
RUN pip install --upgrade pip
RUN pip install --no-cache-dir flask flask-api kafka-python ifaddr 
COPY api.py ./
COPY kafka_ingest.py ./
CMD [ "python", "api.py"]
