"""
Kafka Consumer for Network Metrics
Consumes messages and stores in MySQL database
"""
from kafka import KafkaConsumer
from kafka.errors import KafkaError
import json
import logging
from datetime import datetime
from config import Config
from database import DatabaseManager

logger = logging.getLogger(__name__)


class NetworkMetricsConsumer:
    """Kafka consumer for network metrics"""
    
    def __init__(self):
        """Initialize Kafka Consumer and Database connection"""
        try:
            self.consumer = KafkaConsumer(
                Config.KAFKA_TOPIC,
                **Config.CONSUMER_CONFIG,
                value_deserializer=lambda m: json.loads(m.decode('utf-8'))
            )
            
            self.db = DatabaseManager()
            logger.info("Kafka Consumer initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize consumer: {e}")
            raise
    
    def validate_metric(self, metric):
        """
        Validate metric data
        
        Args:
            metric (dict): Metric data to validate
            
        Returns:
            bool: True if valid, False otherwise
        """
        required_fields = [
            'device_ip', 'timestamp', 'cpu_usage', 'memory_usage',
            'bandwidth_in', 'bandwidth_out', 'packet_loss', 'latency'
        ]
        
        for field in required_fields:
            if field not in metric:
                logger.warning(f"Missing required field: {field}")
                return False
        
        # Validate data types and ranges
        try:
            if not (0 <= metric['cpu_usage'] <= 100):
                return False
            if not (0 <= metric['memory_usage'] <= 100):
                return False
            if metric['bandwidth_in'] < 0 or metric['bandwidth_out'] < 0:
                return False
        except (TypeError, ValueError):
            return False
        
        return True
    
    def process_metric(self, metric):
        """
        Process and store metric in database
        
        Args:
            metric (dict): Metric data to process
            
        Returns:
            bool: True if successful, False otherwise
        """
        if not self.validate_metric(metric):
            logger.warning(f"Invalid metric data: {metric}")
            return False
        
        try:
            success = self.db.store_metric(metric)
            
            if success:
                logger.info(f"Successfully stored metric for device {metric['device_ip']}")
                
                # Check for alerts
                self.check_alerts(metric)
            else:
                logger.error(f"Failed to store metric for device {metric['device_ip']}")
            
            return success
            
        except Exception as e:
            logger.error(f"Error processing metric: {e}")
            return False
    
    def check_alerts(self, metric):
        """
        Check if metric triggers any alerts
        
        Args:
            metric (dict): Metric data to check
        """
        # CPU usage alert
        if metric['cpu_usage'] > 80:
            logger.warning(
                f"HIGH CPU USAGE ALERT: Device {metric['device_ip']} "
                f"CPU at {metric['cpu_usage']}%"
            )
        
        # Memory usage alert
        if metric['memory_usage'] > 85:
            logger.warning(
                f"HIGH MEMORY USAGE ALERT: Device {metric['device_ip']} "
                f"Memory at {metric['memory_usage']}%"
            )
        
        # Packet loss alert
        if metric['packet_loss'] > 1.0:
            logger.warning(
                f"PACKET LOSS ALERT: Device {metric['device_ip']} "
                f"Loss at {metric['packet_loss']}%"
            )
        
        # Interface down alert
        if metric.get('interface_status') == 'down':
            logger.error(
                f"INTERFACE DOWN ALERT: Device {metric['device_ip']} "
                f"Interface is DOWN"
            )
    
    def run(self):
        """Main consumer loop"""
        logger.info("Starting message consumption...")
        
        try:
            for message in self.consumer:
                try:
                    metric = message.value
                    logger.debug(
                        f"Received metric: Topic={message.topic}, "
                        f"Partition={message.partition}, "
                        f"Offset={message.offset}"
                    )
                    
                    self.process_metric(metric)
                    
                except Exception as e:
                    logger.error(f"Error processing message: {e}")
                    continue
                
        except KeyboardInterrupt:
            logger.info("Shutting down consumer...")
        finally:
            self.consumer.close()
            self.db.close()
            logger.info("Consumer shut down complete")


def main():
    """Main entry point for consumer"""
    consumer = NetworkMetricsConsumer()
    consumer.run()


if __name__ == '__main__':
    main()
