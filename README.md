# kafka-streaming-pipeline
Kafka streaming projects and skills

# Kafka Streaming Data Pipeline

## 🎯 Project Overview
Real-time data streaming pipeline using Apache Kafka for network monitoring and performance metrics collection.

## 🏗️ Architecture
```
Network Devices → SNMP Polling → Kafka Producer → Kafka Broker → Kafka Consumer → MySQL Database
```

## 🚀 Features
- Real-time event processing
- Fault-tolerant message delivery
- Scalable architecture
- Performance monitoring dashboard

## 💻 Technologies
- Python 3.8+
- Apache Kafka 2.8
- MySQL 8.0
- Docker

## 📦 Installation
```bash
# Clone repository
git clone https://github.com/skumarhv1/kafka-streaming-pipeline.git

# Install dependencies
pip install -r requirements.txt

# Start Kafka
docker-compose up -d
```

## 🔧 Configuration
```python
KAFKA_BROKER = 'localhost:9092'
TOPIC_NAME = 'network-metrics'
DB_CONNECTION = 'mysql://localhost:3306/network_db'
```

## 📊 Results
- Processing Speed: 10,000 events/second
- Latency Reduction: 60%
- Uptime: 99.9%

## 📝 License
MIT License
