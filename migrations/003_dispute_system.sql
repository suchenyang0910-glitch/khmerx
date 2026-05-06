-- KhmerX Dispute System Upgrade (PostgreSQL)

ALTER TABLE IF EXISTS disputes
ADD COLUMN IF NOT EXISTS offer_id UUID NULL,
ADD COLUMN IF NOT EXISTS borrower_id UUID NULL,
ADD COLUMN IF NOT EXISTS lender_id UUID NULL,
ADD COLUMN IF NOT EXISTS dispute_type VARCHAR(50) NULL,
ADD COLUMN IF NOT EXISTS priority VARCHAR(30) NOT NULL DEFAULT 'normal',
ADD COLUMN IF NOT EXISTS resolution_result VARCHAR(50) NULL,
ADD COLUMN IF NOT EXISTS resolved_by UUID NULL,
ADD COLUMN IF NOT EXISTS resolved_at TIMESTAMP NULL;

CREATE INDEX IF NOT EXISTS idx_disputes_priority
ON disputes(priority);


CREATE TABLE IF NOT EXISTS dispute_evidences (
    id BIGSERIAL PRIMARY KEY,
    dispute_id BIGINT NOT NULL REFERENCES disputes(id) ON DELETE CASCADE,
    uploaded_by_user_id UUID NOT NULL,
    uploaded_role VARCHAR(30) NOT NULL,
    evidence_type VARCHAR(50) NOT NULL,
    file_url TEXT NULL,
    text_note TEXT NULL,
    metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_dispute_evidences_dispute_id
ON dispute_evidences(dispute_id);

