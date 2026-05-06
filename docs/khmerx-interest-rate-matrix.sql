CREATE TABLE IF NOT EXISTS interest_rate_matrix (
    id BIGSERIAL PRIMARY KEY,
    term_days INT NOT NULL,
    credit_level VARCHAR(10) NOT NULL,
    rate_percent NUMERIC(6,2) NOT NULL,
    mode VARCHAR(20) NOT NULL DEFAULT 'cut_interest',
    enabled BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),

    UNIQUE(term_days, credit_level)
);

INSERT INTO interest_rate_matrix
(term_days, credit_level, rate_percent, mode)
VALUES
-- 7 days
(7,  'A', 8.00,  'cut_interest'),
(7,  'B', 9.00,  'cut_interest'),
(7,  'C', 10.00, 'cut_interest'),
(7,  'D', 12.00, 'cut_interest'),

-- 14 days
(14, 'A', 15.00, 'cut_interest'),
(14, 'B', 17.00, 'cut_interest'),
(14, 'C', 18.00, 'cut_interest'),
(14, 'D', 20.00, 'cut_interest'),

-- 30 days
(30, 'A', 25.00, 'cut_interest'),
(30, 'B', 28.00, 'cut_interest'),
(30, 'C', 30.00, 'cut_interest'),
(30, 'D', 35.00, 'cut_interest')
ON CONFLICT (term_days, credit_level)
DO UPDATE SET
    rate_percent = EXCLUDED.rate_percent,
    mode = EXCLUDED.mode,
    updated_at = NOW();

