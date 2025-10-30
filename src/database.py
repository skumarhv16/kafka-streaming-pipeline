"""
Database operations for network metrics storage
"""
import mysql.connector
from mysql.connector import Error, pooling
import logging
from config import Config

logger = logging.getLogger(__name__)


class DatabaseManager:
    """MySQL database manager for network metrics"""
    
    def __init__(self):
        """Initialize database connection pool"""
        try:
            self.pool = pooling.MySQLConnectionPool(
                pool_name="metrics_pool",
                pool_size=5,
                **Config.DB_CONFIG
            )
            
            self.create_tables()
            logger.info("Database connection pool initialized")
            
        except Error as e:
            logger.error(f"Database initialization error: {e}")
            raise
    
    def get_connection(self):
        """Get connection from pool"""
        try:
            return self.pool.get_connection()
        except Error as e:
            logger.error(f"Failed to get connection from pool: {e}")
            raise
    
    def create_tables(self):
        """Create necessary database tables"""
        create_metrics_table = """
        CREATE TABLE IF NOT EXISTS network_metrics (
            id INT AUTO_INCREMENT PRIMARY KEY,
            device_ip VARCHAR(15) NOT NULL,
            timestamp DATETIME NOT NULL,
            cpu_usage FLOAT,
            memory_usage FLOAT,
            bandwidth_in BIGINT,
            bandwidth_out BIGINT,
            packet_loss FLOAT,
            latency FLOAT,
            interface_status VARCHAR(10),
            error_count INT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            INDEX idx_device_timestamp (device_ip, timestamp),
            INDEX idx_timestamp (timestamp)
        )
        """
        
        try:
            connection = self.get_connection()
            cursor = connection.cursor()
            cursor.execute(create_metrics_table)
            connection.commit()
            cursor.close()
            connection.close()
            logger.info("Database tables verified/created")
            
        except Error as e:
            logger.error(f"Failed to create tables: {e}")
            raise
    
    def store_metric(self, metric):
        """
        Store metric in database
        
        Args:
            metric (dict): Metric data to store
            
        Returns:
            bool: True if successful, False otherwise
        """
        insert_query = """
        INSERT INTO network_metrics 
        (device_ip, timestamp, cpu_usage, memory_usage, 
         bandwidth_in, bandwidth_out, packet_loss, latency,
         interface_status, error_count)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        try:
            connection = self.get_connection()
            cursor = connection.cursor()
            
            values = (
                metric['device_ip'],
                metric['timestamp'],
                metric['cpu_usage'],
                metric['memory_usage'],
                metric['bandwidth_in'],
                metric['bandwidth_out'],
                metric['packet_loss'],
                metric['latency'],
                metric.get('interface_status', 'unknown'),
                metric.get('error_count', 0)
            )
            
            cursor.execute(insert_query, values)
            connection.commit()
            cursor.close()
            connection.close()
            
            return True
            
        except Error as e:
            logger.error(f"Database insert error: {e}")
            return False
    
    def get_latest_metrics(self, device_ip=None, limit=10):
        """
        Get latest metrics from database
        
        Args:
            device_ip (str): Specific device IP (optional)
            limit (int): Number of records to fetch
            
        Returns:
            list: List of metric records
        """
        if device_ip:
            query = """
            SELECT * FROM network_metrics 
            WHERE device_ip = %s 
            ORDER BY timestamp DESC 
            LIMIT %s
            """
            params = (device_ip, limit)
        else:
            query = """
            SELECT * FROM network_metrics 
            ORDER BY timestamp DESC 
            LIMIT %s
            """
            params = (limit,)
        
        try:
            connection = self.get_connection()
            cursor = connection.cursor(dictionary=True)
            cursor.execute(query, params)
            results = cursor.fetchall()
            cursor.close()
            connection.close()
            
            return results
            
        except Error as e:
            logger.error(f"Database query error: {e}")
            return []
    
    def close(self):
        """Close database connections"""
        logger.info("Closing database connections")
