-- KhmerX Operator/Agent/Collector V1 (PostgreSQL)

ALTER TABLE IF EXISTS users
ADD COLUMN IF NOT EXISTS sub_role VARCHAR(20) NULL,
ADD COLUMN IF NOT EXISTS agent_id UUID NULL,
ADD COLUMN IF NOT EXISTS inviter_id UUID NULL,
ADD COLUMN IF NOT EXISTS commission_rate NUMERIC(5,2) NOT NULL DEFAULT 0;

CREATE INDEX IF NOT EXISTS idx_users_agent_id ON users(agent_id);
CREATE INDEX IF NOT EXISTS idx_users_inviter_id ON users(inviter_id);


ALTER TABLE IF EXISTS p2p_trades
ADD COLUMN IF NOT EXISTS fund_source VARCHAR(20) NOT NULL DEFAULT 'user';

CREATE INDEX IF NOT EXISTS idx_p2p_trades_fund_source ON p2p_trades(fund_source);


CREATE TABLE IF NOT EXISTS agent_commissions (
    id BIGSERIAL PRIMARY KEY,
    agent_id UUID NOT NULL,
    user_id UUID NOT NULL,
    trade_id UUID NOT NULL,
    amount NUMERIC(12,2) NOT NULL,
    commission_type VARCHAR(50) NOT NULL,
    status VARCHAR(30) NOT NULL DEFAULT 'pending',
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    settled_at TIMESTAMP NULL
);

CREATE INDEX IF NOT EXISTS idx_agent_commissions_agent_id ON agent_commissions(agent_id);
CREATE INDEX IF NOT EXISTS idx_agent_commissions_trade_id ON agent_commissions(trade_id);
CREATE INDEX IF NOT EXISTS idx_agent_commissions_status ON agent_commissions(status);


CREATE TABLE IF NOT EXISTS agent_stats (
    agent_id UUID PRIMARY KEY,
    total_users INT NOT NULL DEFAULT 0,
    total_loans INT NOT NULL DEFAULT 0,
    total_volume NUMERIC(12,2) NOT NULL DEFAULT 0,
    total_commission NUMERIC(12,2) NOT NULL DEFAULT 0,
    pending_commission NUMERIC(12,2) NOT NULL DEFAULT 0,
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);


CREATE TABLE IF NOT EXISTS collection_tasks (
    id BIGSERIAL PRIMARY KEY,
    user_id UUID NOT NULL,
    trade_id UUID NOT NULL,
    agent_id UUID NULL,
    assigned_to UUID NULL,
    status VARCHAR(30) NOT NULL DEFAULT 'pending',
    priority VARCHAR(30) NOT NULL DEFAULT 'normal',
    note TEXT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_collection_tasks_status ON collection_tasks(status);
CREATE INDEX IF NOT EXISTS idx_collection_tasks_trade_id ON collection_tasks(trade_id);
CREATE INDEX IF NOT EXISTS idx_collection_tasks_assigned_to ON collection_tasks(assigned_to);

