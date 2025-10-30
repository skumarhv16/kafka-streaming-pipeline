"""
Configuration management for Kafka pipeline
"""
import os
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Logging configuration
logging.basicConfig(
    level=os.getenv('LOG_LEVEL', 'INFO'),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

class Config:
    """Application configuration"""
    
    # Kafka Configuration
    KAFKA_BOOTSTRAP_SERVERS = os.getenv('KAFKA_BROKER', 'localhost:9092')
    KAFKA_TOPIC = os.getenv('KAFKA_TOPIC', 'network-metrics')
    KAFKA_GROUP_ID = 'network-metrics-consumer-group'
    
    # Producer Configuration
    PRODUCER_CONFIG = {
        'bootstrap_servers': KAFKA_BOOTSTRAP_SERVERS,
        'acks': 'all',
        'retries': 3,
        'max_in_flight_requests_per_connection': 1,
        'compression_type': 'gzip'
    }
    
    # Consumer Configuration
    CONSUMER_CONFIG = {
        'bootstrap_servers': KAFKA_BOOTSTRAP_SERVERS,
        'group_id': KAFKA_GROUP_ID,
        'auto_offset_reset': 'earliest',
        'enable_auto_commit': True,
        'max_poll_records': 500
    }
    
    # Database Configuration
    DB_CONFIG = {
        'host': os.getenv('DB_HOST', 'localhost'),
        'port': int(os.getenv('DB_PORT', 3306)),
        'user': os.getenv('DB_USER', 'root'),
        'password': os.getenv('DB_PASSWORD', ''),
        'database': os.getenv('DB_NAME', 'network_db')
    }
    
    # SNMP Configuration
    SNMP_COMMUNITY = os.getenv('SNMP_COMMUNITY', 'public')
    SNMP_PORT = int(os.getenv('SNMP_PORT', 161))
    POLL_INTERVAL = int(os.getenv('POLL_INTERVAL', 60))
    
    # Application Settings
    MAX_RETRIES = 3
    RETRY_DELAY = 5
    BATCH_SIZE = 100
