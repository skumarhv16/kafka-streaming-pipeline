"""
Unit tests for Kafka Producer
"""
import unittest
from unittest.mock import Mock, patch, MagicMock
from src.producer import NetworkMetricsProducer
import json


class TestNetworkMetricsProducer(unittest.TestCase):
    """Test cases for NetworkMetricsProducer"""
    
    def setUp(self):
        """Set up test fixtures"""
        with patch('src.producer.KafkaProducer'):
            self.producer = NetworkMetricsProducer()
    
    def test_collect_metrics(self):
        """Test metric collection"""
        metrics = self.producer.collect_metrics('192.168.1.1')
        
        # Check required fields
        self.assertIn('device_ip', metrics)
        self.assertIn('timestamp', metrics)
        self.assertIn('cpu_usage', metrics)
        self.assertIn('memory_usage', metrics)
        self.assertIn('bandwidth_in', metrics)
        self.assertIn('bandwidth_out', metrics)
        
        # Check data types
        self.assertIsInstance(metrics['cpu_usage'], float)
        self.assertIsInstance(metrics['memory_usage'], float)
        self.assertIsInstance(metrics['bandwidth_in'], int)
        
        # Check value ranges
        self.assertTrue(0 <= metrics['cpu_usage'] <= 100)
        self.assertTrue(0 <= metrics['memory_usage'] <= 100)
    
    def test_metrics_format(self):
        """Test metrics format is correct"""
        metrics = self.producer.collect_metrics('192.168.1.1')
        
        # Ensure can be JSON serialized
        try:
            json.dumps(metrics)
        except TypeError:
            self.fail("Metrics cannot be JSON serialized")
    
    @patch('src.producer.KafkaProducer')
    def test_send_metrics_success(self, mock_producer):
        """Test successful metric sending"""
        mock_future = MagicMock()
        mock_future.get.return_value = Mock(
            topic='network-metrics',
            partition=0,
            offset=123
        )
        
        self.producer.producer.send.return_value = mock_future
        
        metrics = {'device_ip': '192.168.1.1', 'cpu_usage': 50}
        result = self.producer.send_metrics(metrics)
        
        self.assertTrue(result)
        self.producer.producer.send.assert_called_once()


class TestMetricsValidation(unittest.TestCase):
    """Test metric validation"""
    
    def test_valid_device_ip(self):
        """Test valid device IP format"""
        valid_ips = ['192.168.1.1', '10.0.0.1', '172.16.0.1']
        for ip in valid_ips:
            with patch('src.producer.KafkaProducer'):
                producer = NetworkMetricsProducer()
                metrics = producer.collect_metrics(ip)
                self.assertEqual(metrics['device_ip'], ip)


if __name__ == '__main__':
    unittest.main()
