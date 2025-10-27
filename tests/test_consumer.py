"""
Unit tests for Kafka Consumer
"""
import unittest
from unittest.mock import Mock, patch, MagicMock
from src.consumer import NetworkMetricsConsumer


class TestNetworkMetricsConsumer(unittest.TestCase):
    """Test cases for NetworkMetricsConsumer"""
    
    def setUp(self):
        """Set up test fixtures"""
        with patch('src.consumer.KafkaConsumer'), \
             patch('src.consumer.DatabaseManager'):
            self.consumer = NetworkMetricsConsumer()
    
    def test_validate_metric_valid(self):
        """Test validation with valid metric"""
        valid_metric = {
            'device_ip': '192.168.1.1',
            'timestamp': '2024-11-07T10:00:00',
            'cpu_usage': 50.0,
            'memory_usage': 60.0,
            'bandwidth_in': 1000000,
            'bandwidth_out': 500000,
            'packet_loss': 0.5,
            'latency': 10.0
        }
        
        self.assertTrue(self.consumer.validate_metric(valid_metric))
    
    def test_validate_metric_invalid_cpu(self):
        """Test validation with invalid CPU usage"""
        invalid_metric = {
            'device_ip': '192.168.1.1',
            'timestamp': '2024-11-07T10:00:00',
            'cpu_usage': 150.0,  # Invalid: > 100
            'memory_usage': 60.0,
            'bandwidth_in': 1000000,
            'bandwidth_out': 500000,
            'packet_loss': 0.5,
            'latency': 10.0
        }
        
        self.assertFalse(self.consumer.validate_metric(invalid_metric))
    
    def test_validate_metric_missing_field(self):
        """Test validation with missing required field"""
        invalid_metric = {
            'device_ip': '192.168.1.1',
            'timestamp': '2024-11-07T10:00:00',
            # Missing cpu_usage
            'memory_usage': 60.0,
            'bandwidth_in': 1000000,
            'bandwidth_out': 500000,
            'packet_loss': 0.5,
            'latency': 10.0
        }
        
        self.assertFalse(self.consumer.validate_metric(invalid_metric))


if __name__ == '__main__':
    unittest.main()
