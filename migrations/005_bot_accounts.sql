CREATE TABLE IF NOT EXISTS bot_accounts (
    id BIGSERIAL PRIMARY KEY,
    bot_username VARCHAR(100) NOT NULL UNIQUE,
    bot_token TEXT NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'active',
    is_primary BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_bot_accounts_status
ON bot_accounts(status);

CREATE INDEX IF NOT EXISTS idx_bot_accounts_is_primary
ON bot_accounts(is_primary);
