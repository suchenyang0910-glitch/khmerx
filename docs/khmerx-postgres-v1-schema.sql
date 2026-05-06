-- KhmerX V1 PostgreSQL Schema (greenfield)

CREATE EXTENSION IF NOT EXISTS pgcrypto;

CREATE TABLE users (
    id BIGSERIAL PRIMARY KEY,
    global_user_id UUID NOT NULL DEFAULT gen_random_uuid(),

    tg_id BIGINT NOT NULL UNIQUE,
    tg_username VARCHAR(100),
    name VARCHAR(255),
    avatar_url TEXT,

    role VARCHAR(30) NOT NULL DEFAULT 'user',
    sub_role VARCHAR(30) DEFAULT 'borrower',

    language VARCHAR(10) DEFAULT 'km',

    phone VARCHAR(50),
    aba_account VARCHAR(100),
    aba_name VARCHAR(255),

    verification_level VARCHAR(30) DEFAULT 'unverified',
    profile_completed BOOLEAN DEFAULT FALSE,

    agent_id BIGINT NULL,
    inviter_id BIGINT NULL,

    status VARCHAR(30) DEFAULT 'active',

    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_users_tg_id ON users(tg_id);
CREATE INDEX idx_users_agent_id ON users(agent_id);
CREATE INDEX idx_users_aba_account ON users(aba_account);
CREATE INDEX idx_users_phone ON users(phone);


CREATE TABLE user_risk_profiles (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL UNIQUE REFERENCES users(id),

    credit_score INT NOT NULL DEFAULT 650,
    credit_level VARCHAR(10) NOT NULL DEFAULT 'C',

    risk_score INT NOT NULL DEFAULT 20,
    risk_level VARCHAR(30) NOT NULL DEFAULT 'normal',

    max_borrow_amount NUMERIC(12,2) NOT NULL DEFAULT 100,
    max_active_trades INT NOT NULL DEFAULT 1,

    cancel_count INT DEFAULT 0,
    overdue_count INT DEFAULT 0,
    default_count INT DEFAULT 0,
    dispute_lost_count INT DEFAULT 0,

    is_blocked BOOLEAN DEFAULT FALSE,
    blocked_until TIMESTAMP NULL,
    block_reason TEXT NULL,

    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_user_risk_profiles_level ON user_risk_profiles(risk_level);
CREATE INDEX idx_user_risk_profiles_score ON user_risk_profiles(credit_score);


CREATE TABLE interest_rate_matrix (
    id BIGSERIAL PRIMARY KEY,
    term_days INT NOT NULL,
    credit_level VARCHAR(10) NOT NULL,
    rate_percent NUMERIC(6,2) NOT NULL,
    mode VARCHAR(30) DEFAULT 'cut_interest',
    enabled BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(term_days, credit_level)
);


CREATE TABLE p2p_offers (
    id BIGSERIAL PRIMARY KEY,
    borrower_id BIGINT NOT NULL REFERENCES users(id),

    amount NUMERIC(12,2) NOT NULL,
    term_days INT NOT NULL,

    rate_percent NUMERIC(6,2) NOT NULL,
    interest NUMERIC(12,2) NOT NULL,
    received_amount NUMERIC(12,2) NOT NULL,
    repay_amount NUMERIC(12,2) NOT NULL,

    fee NUMERIC(12,2) DEFAULT 0,

    status VARCHAR(30) NOT NULL DEFAULT 'pending',
    can_bid BOOLEAN DEFAULT TRUE,

    risk_level VARCHAR(30) DEFAULT 'low',
    manual_review_status VARCHAR(30) DEFAULT 'none',

    note TEXT,

    expired_at TIMESTAMP NULL,
    matched_at TIMESTAMP NULL,

    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_p2p_offers_status ON p2p_offers(status);
CREATE INDEX idx_p2p_offers_borrower_id ON p2p_offers(borrower_id);
CREATE INDEX idx_p2p_offers_created_at ON p2p_offers(created_at);


CREATE TABLE p2p_trades (
    id BIGSERIAL PRIMARY KEY,
    offer_id BIGINT NOT NULL REFERENCES p2p_offers(id),
    borrower_id BIGINT NOT NULL REFERENCES users(id),
    lender_id BIGINT NOT NULL REFERENCES users(id),

    amount NUMERIC(12,2) NOT NULL,
    term_days INT NOT NULL,

    rate_percent NUMERIC(6,2) NOT NULL,
    interest NUMERIC(12,2) NOT NULL,
    received_amount NUMERIC(12,2) NOT NULL,
    repay_amount NUMERIC(12,2) NOT NULL,

    fee NUMERIC(12,2) DEFAULT 0,
    status VARCHAR(30) NOT NULL DEFAULT 'matched',
    fund_source VARCHAR(30) DEFAULT 'user',

    lend_deadline TIMESTAMP NULL,
    lend_confirmed_at TIMESTAMP NULL,
    receive_confirmed_at TIMESTAMP NULL,
    completed_at TIMESTAMP NULL,
    cancelled_at TIMESTAMP NULL,

    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_p2p_trades_status ON p2p_trades(status);
CREATE INDEX idx_p2p_trades_borrower_id ON p2p_trades(borrower_id);
CREATE INDEX idx_p2p_trades_lender_id ON p2p_trades(lender_id);
CREATE INDEX idx_p2p_trades_fund_source ON p2p_trades(fund_source);


CREATE TABLE repayment_schedules (
    id BIGSERIAL PRIMARY KEY,
    trade_id BIGINT NOT NULL REFERENCES p2p_trades(id),
    period INT NOT NULL DEFAULT 1,
    due_at TIMESTAMP NOT NULL,
    principal NUMERIC(12,2) NOT NULL,
    interest NUMERIC(12,2) NOT NULL DEFAULT 0,
    total NUMERIC(12,2) NOT NULL,
    status VARCHAR(30) DEFAULT 'pending',
    paid_at TIMESTAMP NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_repayment_schedules_trade_id ON repayment_schedules(trade_id);
CREATE INDEX idx_repayment_schedules_status ON repayment_schedules(status);
CREATE INDEX idx_repayment_schedules_due_at ON repayment_schedules(due_at);


CREATE TABLE payment_proofs (
    id BIGSERIAL PRIMARY KEY,
    trade_id BIGINT NOT NULL REFERENCES p2p_trades(id),
    schedule_id BIGINT NULL REFERENCES repayment_schedules(id),
    uploaded_by BIGINT NOT NULL REFERENCES users(id),
    proof_type VARCHAR(30) NOT NULL,
    amount NUMERIC(12,2) NOT NULL,
    file_url TEXT NOT NULL,
    note TEXT,
    status VARCHAR(30) DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT NOW(),
    confirmed_at TIMESTAMP NULL
);

CREATE INDEX idx_payment_proofs_trade_id ON payment_proofs(trade_id);
CREATE INDEX idx_payment_proofs_uploaded_by ON payment_proofs(uploaded_by);


CREATE TABLE disputes (
    id BIGSERIAL PRIMARY KEY,
    trade_id BIGINT NOT NULL REFERENCES p2p_trades(id),
    offer_id BIGINT NULL REFERENCES p2p_offers(id),
    borrower_id BIGINT NOT NULL REFERENCES users(id),
    lender_id BIGINT NOT NULL REFERENCES users(id),
    raised_by_user_id BIGINT NOT NULL REFERENCES users(id),
    raised_role VARCHAR(30) NOT NULL,
    dispute_type VARCHAR(50) NOT NULL,
    reason TEXT NOT NULL,
    status VARCHAR(30) DEFAULT 'open',
    priority VARCHAR(30) DEFAULT 'normal',
    resolution_result VARCHAR(50),
    resolution_note TEXT,
    resolved_by BIGINT NULL REFERENCES users(id),
    resolved_at TIMESTAMP NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_disputes_trade_id ON disputes(trade_id);
CREATE INDEX idx_disputes_status ON disputes(status);


CREATE TABLE dispute_evidences (
    id BIGSERIAL PRIMARY KEY,
    dispute_id BIGINT NOT NULL REFERENCES disputes(id) ON DELETE CASCADE,
    uploaded_by_user_id BIGINT NOT NULL REFERENCES users(id),
    evidence_type VARCHAR(50) NOT NULL,
    file_url TEXT,
    text_note TEXT,
    metadata JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMP DEFAULT NOW()
);


CREATE TABLE risk_logs (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NULL REFERENCES users(id),
    trade_id BIGINT NULL REFERENCES p2p_trades(id),
    offer_id BIGINT NULL REFERENCES p2p_offers(id),
    event_type VARCHAR(100) NOT NULL,
    risk_action VARCHAR(100),
    score_change INT DEFAULT 0,
    old_score INT,
    new_score INT,
    old_risk_level VARCHAR(30),
    new_risk_level VARCHAR(30),
    reason TEXT,
    metadata JSONB DEFAULT '{}'::jsonb,
    created_by VARCHAR(50) DEFAULT 'system',
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_risk_logs_user_id ON risk_logs(user_id);
CREATE INDEX idx_risk_logs_event_type ON risk_logs(event_type);


CREATE TABLE risk_events (
    id BIGSERIAL PRIMARY KEY,
    event_key UUID DEFAULT gen_random_uuid(),
    event_type VARCHAR(100) NOT NULL,
    user_id BIGINT NULL REFERENCES users(id),
    trade_id BIGINT NULL REFERENCES p2p_trades(id),
    offer_id BIGINT NULL REFERENCES p2p_offers(id),
    severity VARCHAR(30) DEFAULT 'low',
    status VARCHAR(30) DEFAULT 'pending',
    payload JSONB DEFAULT '{}'::jsonb,
    handled_by VARCHAR(50),
    handled_at TIMESTAMP NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_risk_events_status ON risk_events(status);
CREATE INDEX idx_risk_events_severity ON risk_events(severity);


CREATE TABLE device_fingerprints (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL REFERENCES users(id),
    tg_id BIGINT,
    device_id VARCHAR(255),
    ip_hash VARCHAR(255),
    user_agent_hash VARCHAR(255),
    fingerprint_hash VARCHAR(255),
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_device_fingerprints_user_id ON device_fingerprints(user_id);
CREATE INDEX idx_device_fingerprints_fingerprint_hash ON device_fingerprints(fingerprint_hash);


CREATE TABLE user_relation_edges (
    id BIGSERIAL PRIMARY KEY,
    user_a BIGINT NOT NULL REFERENCES users(id),
    user_b BIGINT NOT NULL REFERENCES users(id),
    relation_type VARCHAR(50) NOT NULL,
    weight INT DEFAULT 1,
    evidence JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(user_a, user_b, relation_type)
);

CREATE INDEX idx_user_relation_edges_a ON user_relation_edges(user_a);
CREATE INDEX idx_user_relation_edges_b ON user_relation_edges(user_b);


CREATE TABLE manual_review_cases (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NULL REFERENCES users(id),
    trade_id BIGINT NULL REFERENCES p2p_trades(id),
    offer_id BIGINT NULL REFERENCES p2p_offers(id),
    reason TEXT NOT NULL,
    risk_score INT DEFAULT 0,
    status VARCHAR(30) DEFAULT 'pending',
    decision VARCHAR(30),
    reviewed_by BIGINT NULL REFERENCES users(id),
    review_note TEXT,
    reviewed_at TIMESTAMP NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_manual_review_cases_status ON manual_review_cases(status);


CREATE TABLE agent_commissions (
    id BIGSERIAL PRIMARY KEY,
    agent_id BIGINT NOT NULL REFERENCES users(id),
    user_id BIGINT NOT NULL REFERENCES users(id),
    trade_id BIGINT NOT NULL REFERENCES p2p_trades(id),
    amount NUMERIC(12,2) NOT NULL,
    commission_type VARCHAR(50) NOT NULL,
    status VARCHAR(30) DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT NOW(),
    settled_at TIMESTAMP NULL
);

CREATE INDEX idx_agent_commissions_agent_id ON agent_commissions(agent_id);
CREATE INDEX idx_agent_commissions_status ON agent_commissions(status);


CREATE TABLE collection_tasks (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL REFERENCES users(id),
    trade_id BIGINT NOT NULL REFERENCES p2p_trades(id),
    assigned_to BIGINT NULL REFERENCES users(id),
    agent_id BIGINT NULL REFERENCES users(id),
    status VARCHAR(30) DEFAULT 'pending',
    priority VARCHAR(30) DEFAULT 'normal',
    note TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    completed_at TIMESTAMP NULL
);

CREATE INDEX idx_collection_tasks_status ON collection_tasks(status);
CREATE INDEX idx_collection_tasks_assigned_to ON collection_tasks(assigned_to);


CREATE TABLE platform_fund_pools (
    id BIGSERIAL PRIMARY KEY,
    pool_name VARCHAR(100) DEFAULT 'main',
    total_capital NUMERIC(12,2) DEFAULT 0,
    available_capital NUMERIC(12,2) DEFAULT 0,
    outstanding_principal NUMERIC(12,2) DEFAULT 0,
    overdue_principal NUMERIC(12,2) DEFAULT 0,
    defaulted_principal NUMERIC(12,2) DEFAULT 0,
    daily_lending_limit NUMERIC(12,2) DEFAULT 0,
    daily_lent_amount NUMERIC(12,2) DEFAULT 0,
    status VARCHAR(30) DEFAULT 'healthy',
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);


CREATE TABLE platform_fund_transactions (
    id BIGSERIAL PRIMARY KEY,
    pool_id BIGINT NOT NULL REFERENCES platform_fund_pools(id),
    trade_id BIGINT NULL REFERENCES p2p_trades(id),
    user_id BIGINT NULL REFERENCES users(id),
    tx_type VARCHAR(50) NOT NULL,
    amount NUMERIC(12,2) NOT NULL,
    note TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);


CREATE TABLE notifications (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL REFERENCES users(id),
    type VARCHAR(50) NOT NULL,
    title VARCHAR(255) NOT NULL,
    body TEXT NOT NULL,
    target_type VARCHAR(50),
    target_id BIGINT,
    read BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_notifications_user_id ON notifications(user_id);
CREATE INDEX idx_notifications_read ON notifications(read);


CREATE TABLE bot_accounts (
    id BIGSERIAL PRIMARY KEY,
    bot_username VARCHAR(100) NOT NULL,
    bot_token_encrypted TEXT NOT NULL,
    status VARCHAR(30) DEFAULT 'active',
    is_primary BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);


CREATE TABLE platform_daily_reports (
    id BIGSERIAL PRIMARY KEY,
    report_date DATE NOT NULL UNIQUE,
    new_users INT DEFAULT 0,
    new_borrowers INT DEFAULT 0,
    new_lenders INT DEFAULT 0,
    offer_count INT DEFAULT 0,
    matched_trade_count INT DEFAULT 0,
    completed_trade_count INT DEFAULT 0,
    total_trade_volume NUMERIC(12,2) DEFAULT 0,
    platform_revenue NUMERIC(12,2) DEFAULT 0,
    lender_interest NUMERIC(12,2) DEFAULT 0,
    overdue_amount NUMERIC(12,2) DEFAULT 0,
    defaulted_amount NUMERIC(12,2) DEFAULT 0,
    overdue_rate NUMERIC(8,4) DEFAULT 0,
    default_rate NUMERIC(8,4) DEFAULT 0,
    platform_fund_volume NUMERIC(12,2) DEFAULT 0,
    user_fund_volume NUMERIC(12,2) DEFAULT 0,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

