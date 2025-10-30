# Detailed Setup Guide

## Prerequisites

### System Requirements
- Python 3.8 or higher
- Docker 20.10+
- Docker Compose 1.29+
- 4GB RAM minimum
- 10GB disk space

### Software Installation

#### Install Python
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install python3 python3-pip python3-venv

# macOS
brew install python3

# Windows
# Download from python.org
```

#### Install Docker
```bash
# Ubuntu/Debian
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# macOS/Windows
# Download Docker Desktop from docker.com
```

## Step-by-Step Setup

### 1. Clone Repository
```bash
git clone https://github.com/YOUR-USERNAME/kafka-streaming-pipeline.git
cd kafka-streaming-pipeline
```

### 2. Create Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configure Environment
```bash
cp .env.example .env
# Edit .env with your configurations
nano .env
```

### 5. Start Infrastructure
```bash
# Start all services
docker-compose up -d

# Verify services
docker-compose ps

# Expected output:
# NAME        STATUS          PORTS
# kafka       Up              0.0.0.0:9092->9092/tcp
# zookeeper   Up              0.0.0.0:2181->2181/tcp
# mysql       Up              0.0.0.0:3306->3306/tcp
```

### 6. Verify Kafka
```bash
# List topics
docker exec kafka kafka-topics.sh --list --bootstrap-server localhost:9092

# Should show: network-metrics
```

### 7. Verify MySQL
```bash
# Connect to MySQL
docker exec -it mysql mysql -u root -p
# Password: rootpassword

# Check database
SHOW DATABASES;
USE network_db;
SHOW TABLES;
```

### 8. Run Tests
```bash
pytest tests/ -v
```

### 9. Start Application
```bash
# Terminal 1: Start Producer
python src/producer.py

# Terminal 2: Start Consumer
python src/consumer.py
```

## Troubleshooting

### Kafka Won't Start
```bash
# Check logs
docker logs kafka

# Restart
docker-compose restart kafka
```

### Database Connection Error
```bash
# Check MySQL logs
docker logs mysql

# Verify connection
docker exec mysql mysqladmin -u root -p status
```

### Port Already in Use
```bash
# Find process using port
lsof -i :9092  # macOS/Linux
netstat -ano | findstr :9092  # Windows

# Kill process or change port in docker-compose.yml
```

## Next Steps

1. Customize SNMP polling logic
2. Add custom alerting rules
3. Set up monitoring dashboard
4. Configure production database
5. Implement authentication
