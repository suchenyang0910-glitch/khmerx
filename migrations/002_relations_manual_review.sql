-- KhmerX Relations + Manual Review (PostgreSQL)

ALTER TABLE IF EXISTS user_risk_profiles
ADD COLUMN IF NOT EXISTS risk_score INT NOT NULL DEFAULT 0;

CREATE TABLE IF NOT EXISTS user_relation_edges (
    id BIGSERIAL PRIMARY KEY,
    user_a UUID NOT NULL,
    user_b UUID NOT NULL,
    relation_type VARCHAR(50) NOT NULL,
    weight INT NOT NULL DEFAULT 1,
    evidence JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    UNIQUE(user_a, user_b, relation_type)
);

CREATE INDEX IF NOT EXISTS idx_user_relation_edges_pair
ON user_relation_edges(user_a, user_b);

CREATE INDEX IF NOT EXISTS idx_user_relation_edges_type
ON user_relation_edges(relation_type);


CREATE TABLE IF NOT EXISTS risk_score_logs (
    id BIGSERIAL PRIMARY KEY,
    user_id UUID NOT NULL,
    score_change INT NOT NULL,
    old_score INT NULL,
    new_score INT NULL,
    reason TEXT NULL,
    created_by VARCHAR(50) NOT NULL DEFAULT 'system',
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_risk_score_logs_user_id
ON risk_score_logs(user_id);

CREATE INDEX IF NOT EXISTS idx_risk_score_logs_created_at
ON risk_score_logs(created_at);


CREATE TABLE IF NOT EXISTS manual_review_cases (
    id BIGSERIAL PRIMARY KEY,
    user_id UUID NULL,
    trade_id UUID NULL,
    offer_id UUID NULL,
    reason TEXT NOT NULL,
    risk_score INT NOT NULL DEFAULT 0,
    status VARCHAR(30) NOT NULL DEFAULT 'pending',
    decision VARCHAR(30) NULL,
    reviewed_by UUID NULL,
    review_note TEXT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    reviewed_at TIMESTAMP NULL
);

CREATE INDEX IF NOT EXISTS idx_manual_review_cases_status
ON manual_review_cases(status);

CREATE INDEX IF NOT EXISTS idx_manual_review_cases_created_at
ON manual_review_cases(created_at);

