# File: kafka_producer.py
from kafka import KafkaProducer
import json
import time

class NetworkMetricsProducer:
    def __init__(self, bootstrap_servers):
        self.producer = KafkaProducer(
            bootstrap_servers=bootstrap_servers,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )
    
    def send_metric(self, topic, metric_data):
        """Send network metric to Kafka topic"""
        self.producer.send(topic, metric_data)
        self.producer.flush()

# File: kafka_consumer.py
from kafka import KafkaConsumer
import json
import mysql.connector

class NetworkMetricsConsumer:
    def __init__(self, bootstrap_servers, topic):
        self.consumer = KafkaConsumer(
            topic,
            bootstrap_servers=bootstrap_servers,
            value_deserializer=lambda m: json.loads(m.decode('utf-8'))
        )
    
    def process_messages(self):
        """Process messages and store in database"""
        for message in self.consumer:
            self.store_metric(message.value)
    
    def store_metric(self, metric):
        """Store metric in MySQL database"""
        # Database insertion logic
        pass
