CREATE SCHEMA IF NOT EXISTS user_center;

CREATE TABLE IF NOT EXISTS user_center.users (
    id BIGSERIAL PRIMARY KEY,
    uid VARCHAR(64) UNIQUE NOT NULL,
    phone VARCHAR(32),
    email VARCHAR(128),
    real_name VARCHAR(128),
    id_number VARCHAR(64),
    face_verify_status SMALLINT DEFAULT 0,
    risk_level VARCHAR(32),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
COMMENT ON TABLE user_center.users IS '用户表';

CREATE SCHEMA IF NOT EXISTS merchant_center;

CREATE TABLE IF NOT EXISTS merchant_center.merchants (
    merchant_id VARCHAR(64) PRIMARY KEY,
    company_name VARCHAR(128) NOT NULL,
    business_license VARCHAR(128),
    industry_type VARCHAR(64),
    api_key VARCHAR(128) UNIQUE,
    saas_version VARCHAR(32),
    status SMALLINT DEFAULT 1,
    expire_time TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
COMMENT ON TABLE merchant_center.merchants IS '商户表';

CREATE SCHEMA IF NOT EXISTS risk_engine;

CREATE TABLE IF NOT EXISTS risk_engine.risk_orders (
    order_id VARCHAR(64) PRIMARY KEY,
    merchant_id VARCHAR(64) NOT NULL,
    user_id VARCHAR(64) NOT NULL,
    scenario_type VARCHAR(64),
    apply_amount DECIMAL(16, 2),
    risk_score DECIMAL(5, 2),
    risk_level VARCHAR(32),
    approve_status VARCHAR(32),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
COMMENT ON TABLE risk_engine.risk_orders IS '风控订单表';

CREATE TABLE IF NOT EXISTS risk_engine.risk_rules (
    rule_id VARCHAR(64) PRIMARY KEY,
    rule_name VARCHAR(128) NOT NULL,
    scenario_type VARCHAR(64),
    rule_expression TEXT,
    score_weight DECIMAL(5, 2),
    risk_action VARCHAR(64),
    status SMALLINT DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
COMMENT ON TABLE risk_engine.risk_rules IS '风控规则表';

CREATE TABLE IF NOT EXISTS risk_engine.risk_tags (
    tag_id VARCHAR(64) PRIMARY KEY,
    tag_name VARCHAR(64) NOT NULL,
    risk_weight DECIMAL(5, 2),
    tag_category VARCHAR(64),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
COMMENT ON TABLE risk_engine.risk_tags IS '风险标签表';

CREATE SCHEMA IF NOT EXISTS blacklist_center;

CREATE TABLE IF NOT EXISTS blacklist_center.blacklist_subjects (
    subject_id VARCHAR(128) PRIMARY KEY,
    subject_type VARCHAR(32) NOT NULL,
    blacklist_reason VARCHAR(255),
    risk_level VARCHAR(32),
    reported_by VARCHAR(64),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
COMMENT ON TABLE blacklist_center.blacklist_subjects IS '黑名单主体表';

CREATE SCHEMA IF NOT EXISTS device_center;

CREATE TABLE IF NOT EXISTS device_center.device_fingerprints (
    device_id VARCHAR(128) PRIMARY KEY,
    fingerprint_hash VARCHAR(256) UNIQUE NOT NULL,
    ip_address VARCHAR(64),
    gps_location VARCHAR(128),
    browser_info TEXT,
    risk_score DECIMAL(5, 2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
COMMENT ON TABLE device_center.device_fingerprints IS '设备指纹表';

CREATE SCHEMA IF NOT EXISTS api_center;

CREATE TABLE IF NOT EXISTS api_center.api_logs (
    log_id VARCHAR(64) PRIMARY KEY,
    merchant_id VARCHAR(64),
    api_name VARCHAR(128),
    request_body TEXT,
    response_body TEXT,
    response_time INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
COMMENT ON TABLE api_center.api_logs IS 'API调用日志表';

CREATE SCHEMA IF NOT EXISTS billing_center;

CREATE TABLE IF NOT EXISTS billing_center.billing_orders (
    billing_id VARCHAR(64) PRIMARY KEY,
    merchant_id VARCHAR(64) NOT NULL,
    billing_type VARCHAR(64),
    total_amount DECIMAL(16, 2),
    effect_rate DECIMAL(5, 2),
    settlement_status VARCHAR(32),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
COMMENT ON TABLE billing_center.billing_orders IS '账单表';
