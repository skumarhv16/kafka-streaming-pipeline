"""
Kafka Producer for Network Metrics
Collects SNMP data and publishes to Kafka
"""
from kafka import KafkaProducer
from kafka.errors import KafkaError
import json
import time
import logging
import random
from datetime import datetime
from config import Config

logger = logging.getLogger(__name__)


class NetworkMetricsProducer:
    """Kafka producer for network metrics"""
    
    def __init__(self):
        """Initialize Kafka Producer"""
        try:
            self.producer = KafkaProducer(
                **Config.PRODUCER_CONFIG,
                value_serializer=lambda v: json.dumps(v).encode('utf-8')
            )
            logger.info("Kafka Producer initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize producer: {e}")
            raise
    
    def collect_metrics(self, device_ip):
        """
        Simulate SNMP polling to collect network metrics
        In production, use pysnmp library for actual SNMP polling
        
        Args:
            device_ip (str): IP address of the network device
            
        Returns:
            dict: Network metrics data
        """
        # Simulated metrics - replace with actual SNMP polling in production
        metrics = {
            'device_ip': device_ip,
            'timestamp': datetime.now().isoformat(),
            'cpu_usage': round(random.uniform(10, 90), 2),
            'memory_usage': round(random.uniform(20, 85), 2),
            'bandwidth_in': random.randint(100000, 10000000),
            'bandwidth_out': random.randint(50000, 5000000),
            'packet_loss': round(random.uniform(0, 2), 2),
            'latency': round(random.uniform(1, 50), 2),
            'interface_status': random.choice(['up', 'up', 'up', 'down']),
            'error_count': random.randint(0, 10)
        }
        
        logger.debug(f"Collected metrics for device {device_ip}")
        return metrics
    
    def send_metrics(self, metrics):
        """
        Send metrics to Kafka topic
        
        Args:
            metrics (dict): Metrics data to send
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            future = self.producer.send(
                Config.KAFKA_TOPIC,
                value=metrics,
                key=metrics['device_ip'].encode('utf-8')
            )
            
            # Wait for confirmation
            record_metadata = future.get(timeout=10)
            
            logger.info(
                f"Message sent successfully: "
                f"Topic={record_metadata.topic}, "
                f"Partition={record_metadata.partition}, "
                f"Offset={record_metadata.offset}"
            )
            return True
            
        except KafkaError as e:
            logger.error(f"Failed to send message: {e}")
            return False
    
    def run(self, devices):
        """
        Main producer loop
        
        Args:
            devices (list): List of device IP addresses to monitor
        """
        logger.info(f"Starting metrics collection for {len(devices)} devices...")
        
        try:
            while True:
                for device in devices:
                    try:
                        metrics = self.collect_metrics(device)
                        self.send_metrics(metrics)
                    except Exception as e:
                        logger.error(f"Error processing device {device}: {e}")
                
                logger.info(f"Waiting {Config.POLL_INTERVAL} seconds before next poll...")
                time.sleep(Config.POLL_INTERVAL)
                
        except KeyboardInterrupt:
            logger.info("Shutting down producer...")
        finally:
            self.producer.flush()
            self.producer.close()
            logger.info("Producer shut down complete")


def main():
    """Main entry point for producer"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Network Metrics Producer')
    parser.add_argument(
        '--devices',
        nargs='+',
        default=['192.168.1.1', '192.168.1.2', '192.168.1.3'],
        help='List of device IPs to monitor'
    )
    
    args = parser.parse_args()
    
    producer = NetworkMetricsProducer()
    producer.run(args.devices)


if __name__ == '__main__':
    main()
