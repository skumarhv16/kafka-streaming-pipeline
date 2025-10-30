-- Initialize database schema

CREATE DATABASE IF NOT EXISTS network_db;
USE network_db;

-- Network metrics table
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
    INDEX idx_timestamp (timestamp),
    INDEX idx_device (device_ip)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Alerts table
CREATE TABLE IF NOT EXISTS alerts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    device_ip VARCHAR(15) NOT NULL,
    alert_type VARCHAR(50) NOT NULL,
    severity VARCHAR(20) NOT NULL,
    message TEXT,
    triggered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    resolved_at TIMESTAMP NULL,
    INDEX idx_device (device_ip),
    INDEX idx_triggered (triggered_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Device inventory table
CREATE TABLE IF NOT EXISTS devices (
    id INT AUTO_INCREMENT PRIMARY KEY,
    device_ip VARCHAR(15) UNIQUE NOT NULL,
    device_name VARCHAR(100),
    device_type VARCHAR(50),
    location VARCHAR(100),
    status VARCHAR(20) DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_status (status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Insert sample devices
INSERT INTO devices (device_ip, device_name, device_type, location) VALUES
('192.168.1.1', 'Router-Main', 'Router', 'Data Center A'),
('192.168.1.2', 'Switch-Core', 'Switch', 'Data Center A'),
('192.168.1.3', 'Router-Backup', 'Router', 'Data Center B')
ON DUPLICATE KEY UPDATE device_name=VALUES(device_name);
