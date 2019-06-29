from kafka import KafkaProducer, KafkaConsumer
import logging
from time import sleep

logging.basicConfig(level=logging.DEBUG)

topic = "numbers"

producer = KafkaProducer(
					bootstrap_servers=['10.97.55.201:9093']	 
						)
print("got producer")
sleep(4)
for _ in range(100):
	producer.send(topic, b'some_message_bytes')
	sleep(1)

producer.close()

consumer = KafkaConsumer(
            topic,
            bootstrap_servers=['10.97.55.201:9093'],
            auto_offset_reset='earliest',
            consumer_timeout_ms=1000)

print("got here")
for message in consumer:
	print(message)

consumer.close()
