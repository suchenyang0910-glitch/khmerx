-- ==============================================================================
-- KhmerX AI Risk Engine (KX-AIRE) PostgreSQL 16 初始化脚本
-- 根据 KhmerX_AIRE_PRD_V1.md 定义
-- 建议：可以创建不同的 Database，或者在一个 Database 下使用不同 Schema
-- 此处为了演示方便，采用在默认库下创建不同 Schema 的方式
-- ==============================================================================

-- 1. 用户中心数据库 (user_center)
CREATE SCHEMA IF NOT EXISTS user_center;

CREATE TABLE IF NOT EXISTS user_center.users (
    id BIGSERIAL PRIMARY KEY,
    uid VARCHAR(64) UNIQUE NOT NULL,
    phone VARCHAR(32),
    email VARCHAR(128),
    real_name VARCHAR(128),
    id_number VARCHAR(64),
    face_verify_status SMALLINT DEFAULT 0, -- 0:未认证, 1:认证中, 2:认证成功, 3:认证失败
    risk_level VARCHAR(32),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
COMMENT ON TABLE user_center.users IS '用户表';

-- 2. 商户中心数据库 (merchant_center)
CREATE SCHEMA IF NOT EXISTS merchant_center;

CREATE TABLE IF NOT EXISTS merchant_center.merchants (
    merchant_id VARCHAR(64) PRIMARY KEY,
    company_name VARCHAR(128) NOT NULL,
    business_license VARCHAR(128),
    industry_type VARCHAR(64),
    api_key VARCHAR(128) UNIQUE,
    saas_version VARCHAR(32), -- basic, pro, enterprise
    status SMALLINT DEFAULT 1, -- 0:禁用, 1:启用
    expire_time TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
COMMENT ON TABLE merchant_center.merchants IS '商户表';

-- 3. 风控核心数据库 (risk_engine)
CREATE SCHEMA IF NOT EXISTS risk_engine;

CREATE TABLE IF NOT EXISTS risk_engine.risk_orders (
    order_id VARCHAR(64) PRIMARY KEY,
    merchant_id VARCHAR(64) NOT NULL,
    user_id VARCHAR(64) NOT NULL,
    scenario_type VARCHAR(64), -- 例如：phone_rental, house_rental
    apply_amount DECIMAL(16, 2),
    risk_score DECIMAL(5, 2),
    risk_level VARCHAR(32), -- AAA, AA, A, B, C, D
    approve_status VARCHAR(32), -- approved, rejected, manual_review
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
COMMENT ON TABLE risk_engine.risk_orders IS '风控订单表';

CREATE TABLE IF NOT EXISTS risk_engine.risk_rules (
    rule_id VARCHAR(64) PRIMARY KEY,
    rule_name VARCHAR(128) NOT NULL,
    scenario_type VARCHAR(64),
    rule_expression TEXT,
    score_weight DECIMAL(5, 2),
    risk_action VARCHAR(64), -- reject, manual_review, alert
    status SMALLINT DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
COMMENT ON TABLE risk_engine.risk_rules IS '风控规则表';

CREATE TABLE IF NOT EXISTS risk_engine.risk_tags (
    tag_id VARCHAR(64) PRIMARY KEY,
    tag_name VARCHAR(64) NOT NULL,
    risk_weight DECIMAL(5, 2),
    tag_category VARCHAR(64), -- user, device, behavior, relation
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
COMMENT ON TABLE risk_engine.risk_tags IS '风险标签表';

-- 4. 黑名单数据库 (blacklist_center)
CREATE SCHEMA IF NOT EXISTS blacklist_center;

CREATE TABLE IF NOT EXISTS blacklist_center.blacklist_subjects (
    subject_id VARCHAR(128) PRIMARY KEY, -- 可以是身份证号、手机号、设备ID等
    subject_type VARCHAR(32) NOT NULL, -- phone, id_card, device, ip
    blacklist_reason VARCHAR(255),
    risk_level VARCHAR(32),
    reported_by VARCHAR(64), -- 上报商户ID或系统
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
COMMENT ON TABLE blacklist_center.blacklist_subjects IS '黑名单主体表';

-- 5. 设备指纹数据库 (device_center)
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

-- 6. API调用数据库 (api_center)
CREATE SCHEMA IF NOT EXISTS api_center;

CREATE TABLE IF NOT EXISTS api_center.api_logs (
    log_id VARCHAR(64) PRIMARY KEY,
    merchant_id VARCHAR(64),
    api_name VARCHAR(128),
    request_body TEXT,
    response_body TEXT,
    response_time INTEGER, -- 毫秒
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
COMMENT ON TABLE api_center.api_logs IS 'API调用日志表';

-- 7. RaaS计费数据库 (billing_center)
CREATE SCHEMA IF NOT EXISTS billing_center;

CREATE TABLE IF NOT EXISTS billing_center.billing_orders (
    billing_id VARCHAR(64) PRIMARY KEY,
    merchant_id VARCHAR(64) NOT NULL,
    billing_type VARCHAR(64), -- api_call, raas_share, saas_sub
    total_amount DECIMAL(16, 2),
    effect_rate DECIMAL(5, 2),
    settlement_status VARCHAR(32), -- pending, settled, failed
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
COMMENT ON TABLE billing_center.billing_orders IS '账单表';
