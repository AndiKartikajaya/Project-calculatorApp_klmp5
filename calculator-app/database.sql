-- MathHub Calculator Database Schema
-- Created: 2024-01-01

-- Create database
CREATE DATABASE IF NOT EXISTS mathhub_calculator;
USE mathhub_calculator;

-- Users table
CREATE TABLE IF NOT EXISTS users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    INDEX idx_username (username),
    INDEX idx_email (email)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Calculation history table
CREATE TABLE IF NOT EXISTS calculation_history (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    operation_type VARCHAR(50) NOT NULL,
    expression TEXT NOT NULL,
    result VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    
    INDEX idx_user_id (user_id),
    INDEX idx_operation_type (operation_type),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Insert sample data (optional)
INSERT INTO users (username, email, password_hash) VALUES
('john_doe', 'john@example.com', '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW'), -- password: password123
('jane_smith', 'jane@example.com', '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW'),
('test_user', 'test@example.com', '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW');

INSERT INTO calculation_history (user_id, operation_type, expression, result) VALUES
(1, 'addition', '10 + 5', '15'),
(1, 'multiplication', '12 × 3', '36'),
(1, 'division', '100 ÷ 4', '25'),
(2, 'subtraction', '50 - 23', '27'),
(2, 'square_root', '√144', '12'),
(3, 'sin', 'sin(30°)', '0.5'),
(3, 'conversion', '100 km = ? miles', '62.1371'),
(1, 'finance', 'Loan: P=10000, R=5% p.a., T=5 years', '188.71');

-- Create views for reporting
CREATE VIEW user_calculation_stats AS
SELECT 
    u.id as user_id,
    u.username,
    COUNT(ch.id) as total_calculations,
    MIN(ch.created_at) as first_calculation,
    MAX(ch.created_at) as last_calculation
FROM users u
LEFT JOIN calculation_history ch ON u.id = ch.user_id
GROUP BY u.id, u.username;

CREATE VIEW popular_operations AS
SELECT 
    operation_type,
    COUNT(*) as usage_count,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM calculation_history), 2) as percentage
FROM calculation_history
GROUP BY operation_type
ORDER BY usage_count DESC;

-- Stored procedure for cleaning old history
DELIMITER //

CREATE PROCEDURE CleanOldHistory(IN days_old INT)
BEGIN
    DELETE FROM calculation_history 
    WHERE created_at < DATE_SUB(NOW(), INTERVAL days_old DAY);
    
    SELECT ROW_COUNT() AS records_deleted;
END //

DELIMITER ;

-- Function to calculate user activity level
DELIMITER //

CREATE FUNCTION GetUserActivityLevel(user_id INT) 
RETURNS VARCHAR(20)
DETERMINISTIC
BEGIN
    DECLARE calc_count INT;
    DECLARE activity_level VARCHAR(20);
    
    SELECT COUNT(*) INTO calc_count
    FROM calculation_history
    WHERE user_id = user_id
    AND created_at >= DATE_SUB(NOW(), INTERVAL 30 DAY);
    
    IF calc_count >= 100 THEN
        SET activity_level = 'Very Active';
    ELSEIF calc_count >= 50 THEN
        SET activity_level = 'Active';
    ELSEIF calc_count >= 20 THEN
        SET activity_level = 'Moderate';
    ELSEIF calc_count >= 5 THEN
        SET activity_level = 'Light';
    ELSE
        SET activity_level = 'Inactive';
    END IF;
    
    RETURN activity_level;
END //

DELIMITER ;