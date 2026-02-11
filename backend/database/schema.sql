CREATE TABLE attacks (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    ip_address VARCHAR(45) NOT NULL,
    username_attempted VARCHAR(100),
    password_attempted VARCHAR(255),
    country VARCHAR(100),
    user_agent TEXT,
    attack_type VARCHAR(100),
    risk_score INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    INDEX idx_ip_time (ip_address, created_at),
    INDEX idx_created_at (created_at),
    INDEX idx_risk_score (risk_score)
);

CREATE TABLE ip_profile (
    ip_address VARCHAR(45) PRIMARY KEY,
    total_attempts INT DEFAULT 0,
    last_attempt TIMESTAMP,
    threat_level VARCHAR(20),
    is_blocked BOOLEAN DEFAULT FALSE
);
