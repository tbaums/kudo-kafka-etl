FROM python:alpine
WORKDIR /usr/src/app
RUN mkdir -p /usr/src/app/templates
RUN pip install --upgrade pip
RUN pip install --no-cache-dir flask flask-api kafka-python ifaddr 
COPY api.py ./
COPY kafka_ingest.py ./
COPY templates/* /usr/src/app/templates/
CMD [ "python", "api.py"]
