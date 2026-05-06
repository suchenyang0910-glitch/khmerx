-- KhmerX Risk System Init (PostgreSQL)

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- 1. 用户风控档案表
CREATE TABLE IF NOT EXISTS user_risk_profiles (
    id BIGSERIAL PRIMARY KEY,
    user_id UUID NOT NULL UNIQUE,

    risk_level VARCHAR(30) NOT NULL DEFAULT 'normal',
    credit_score INT NOT NULL DEFAULT 650,
    credit_level VARCHAR(10) NOT NULL DEFAULT 'C',

    max_borrow_amount NUMERIC(12,2) NOT NULL DEFAULT 300.00,
    max_active_trades INT NOT NULL DEFAULT 1,

    cancel_count INT NOT NULL DEFAULT 0,
    matched_cancel_count INT NOT NULL DEFAULT 0,
    overdue_count INT NOT NULL DEFAULT 0,
    default_count INT NOT NULL DEFAULT 0,
    dispute_lost_count INT NOT NULL DEFAULT 0,

    is_blocked BOOLEAN NOT NULL DEFAULT FALSE,
    blocked_until TIMESTAMP NULL,
    block_reason TEXT NULL,

    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_user_risk_profiles_user_id
ON user_risk_profiles(user_id);

CREATE INDEX IF NOT EXISTS idx_user_risk_profiles_risk_level
ON user_risk_profiles(risk_level);

CREATE INDEX IF NOT EXISTS idx_user_risk_profiles_credit_level
ON user_risk_profiles(credit_level);


-- 2. 风控日志表
CREATE TABLE IF NOT EXISTS risk_logs (
    id BIGSERIAL PRIMARY KEY,

    user_id UUID NULL,
    trade_id UUID NULL,
    offer_id UUID NULL,

    event_type VARCHAR(100) NOT NULL,
    risk_action VARCHAR(100) NULL,

    score_change INT NOT NULL DEFAULT 0,
    old_score INT NULL,
    new_score INT NULL,

    old_risk_level VARCHAR(30) NULL,
    new_risk_level VARCHAR(30) NULL,

    reason TEXT NULL,
    metadata JSONB NOT NULL DEFAULT '{}'::jsonb,

    created_by VARCHAR(50) NOT NULL DEFAULT 'system',
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_risk_logs_user_id
ON risk_logs(user_id);

CREATE INDEX IF NOT EXISTS idx_risk_logs_trade_id
ON risk_logs(trade_id);

CREATE INDEX IF NOT EXISTS idx_risk_logs_event_type
ON risk_logs(event_type);

CREATE INDEX IF NOT EXISTS idx_risk_logs_created_at
ON risk_logs(created_at);


-- 3. 设备指纹表
CREATE TABLE IF NOT EXISTS device_fingerprints (
    id BIGSERIAL PRIMARY KEY,

    user_id UUID NOT NULL,
    tg_id BIGINT NULL,

    device_id VARCHAR(255) NULL,
    ip_hash VARCHAR(255) NULL,
    user_agent_hash VARCHAR(255) NULL,
    fingerprint_hash VARCHAR(255) NULL,

    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_device_fingerprints_user_id
ON device_fingerprints(user_id);

CREATE INDEX IF NOT EXISTS idx_device_fingerprints_tg_id
ON device_fingerprints(tg_id);

CREATE INDEX IF NOT EXISTS idx_device_fingerprints_fingerprint_hash
ON device_fingerprints(fingerprint_hash);

CREATE INDEX IF NOT EXISTS idx_device_fingerprints_ip_hash
ON device_fingerprints(ip_hash);


-- 4. 风控规则表
CREATE TABLE IF NOT EXISTS risk_rules (
    id BIGSERIAL PRIMARY KEY,

    code VARCHAR(100) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    rule_type VARCHAR(50) NOT NULL,

    threshold_value NUMERIC(12,2) NULL,
    action VARCHAR(100) NOT NULL,
    score_delta INT NOT NULL DEFAULT 0,

    enabled BOOLEAN NOT NULL DEFAULT TRUE,

    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);


-- 5. 初始化规则
INSERT INTO risk_rules
(code, name, rule_type, threshold_value, action, score_delta)
VALUES
('NEW_USER_MAX_AMOUNT', '新用户最大借款金额', 'create_offer', 300, 'manual_review', 0),
('DAILY_OFFER_LIMIT_WATCH', '24小时创建挂单达到3次', 'create_offer', 3, 'mark_watch', 0),
('DAILY_OFFER_LIMIT_FLAGGED', '24小时创建挂单达到5次', 'create_offer', 5, 'mark_flagged', -10),
('CANCEL_LIMIT_3', '连续取消3次', 'cancel_offer', 3, 'block_24h', -10),
('CANCEL_LIMIT_5', '连续取消5次', 'cancel_offer', 5, 'restricted', -20),
('LENDER_NO_PAY_24H', '放款人接单24小时未打款', 'trade_timeout', 24, 'block_24h', -20),
('OVERDUE_ONCE', '出现逾期', 'repayment', 1, 'mark_watch', -20),
('OVERDUE_7_DAYS', '逾期超过7天', 'repayment', 7, 'defaulted', -50),
('DISPUTE_LOST', '仲裁失败', 'dispute', 1, 'mark_flagged', -50),
('FRAUD_CONFIRMED', '确认欺诈', 'admin', 1, 'blocked', -100)
ON CONFLICT (code)
DO UPDATE SET
    name = EXCLUDED.name,
    rule_type = EXCLUDED.rule_type,
    threshold_value = EXCLUDED.threshold_value,
    action = EXCLUDED.action,
    score_delta = EXCLUDED.score_delta,
    updated_at = NOW();


-- 6. Dispute 争议表
CREATE TABLE IF NOT EXISTS disputes (
    id BIGSERIAL PRIMARY KEY,

    trade_id UUID NOT NULL,
    raised_by_user_id UUID NOT NULL,
    raised_role VARCHAR(30) NOT NULL,

    reason TEXT NOT NULL,
    evidence_urls JSONB NOT NULL DEFAULT '[]'::jsonb,

    status VARCHAR(30) NOT NULL DEFAULT 'open',
    resolution_result VARCHAR(50) NULL,
    resolution_note TEXT NULL,
    resolved_by UUID NULL,
    resolved_at TIMESTAMP NULL,

    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_disputes_trade_id
ON disputes(trade_id);

CREATE INDEX IF NOT EXISTS idx_disputes_status
ON disputes(status);


-- 7. 风控事件队列表，给 OpenClaw 读取
CREATE TABLE IF NOT EXISTS risk_events (
    id BIGSERIAL PRIMARY KEY,

    event_key UUID NOT NULL DEFAULT uuid_generate_v4(),
    event_type VARCHAR(100) NOT NULL,

    user_id UUID NULL,
    trade_id UUID NULL,
    offer_id UUID NULL,

    severity VARCHAR(30) NOT NULL DEFAULT 'low',
    status VARCHAR(30) NOT NULL DEFAULT 'pending',

    payload JSONB NOT NULL DEFAULT '{}'::jsonb,

    handled_by VARCHAR(50) NULL,
    handled_at TIMESTAMP NULL,

    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_risk_events_status
ON risk_events(status);

CREATE INDEX IF NOT EXISTS idx_risk_events_severity
ON risk_events(severity);

CREATE INDEX IF NOT EXISTS idx_risk_events_created_at
ON risk_events(created_at);

