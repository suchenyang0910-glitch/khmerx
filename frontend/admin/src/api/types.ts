export type AdminDashboard = {
  users: number
  offers: { pending: number }
  trades: { active: number }
  disputes: { open: number }
  risk: { pending_events: number }
}

export type AdminUser = {
  id: string
  tg_id: number
  name: string
  role: string
  risk_level: string
  credit_score: number
  phone: string | null
  aba_account: string | null
  aba_name: string | null
  created_at: string | null
}

export type AdminOffer = {
  id: string
  borrower_id: string
  amount: number
  term_days: number
  rate: number
  fee: number
  total_amount: number
  status: string
  note: string
  created_at: string | null
}

export type AdminTrade = {
  id: string
  offer_id: string
  borrower_id: string
  lender_id: string
  amount: number
  term_days: number
  rate: number
  fee: number
  total_repayable: number
  status: string
  fund_source: string
  created_at: string | null
}

export type AdminNotification = {
  id: string
  user_id: string
  type: string
  title: string
  body: string
  read: boolean
  created_at: string | null
}

export type AdminInterestRate = {
  id: number
  term_days: number
  credit_level: string
  rate_percent: number
  mode: string
  enabled: boolean
  updated_at: string | null
}

export type AdminRiskEvent = {
  id: number
  event_type: string
  severity: string
  status: string
  user_id: string | null
  trade_id: string | null
  offer_id: string | null
  payload: Record<string, unknown>
  handled_by: string | null
  handled_at: string | null
  created_at: string | null
}

export type AdminRiskRule = {
  id: number
  code: string
  name: string
  rule_type: string
  threshold_value: number | null
  action: string
  score_delta: number
  enabled: boolean
}

export type AdminFlaggedUser = {
  user_id: string
  risk_level: string
  credit_score: number
  credit_level: string
  max_borrow_amount: number
  max_active_trades: number
  is_blocked: boolean
  blocked_until: string | null
  block_reason: string | null
  updated_at: string | null
}

export type AdminDispute = {
  id: number
  trade_id: string
  borrower_id: string | null
  lender_id: string | null
  status: string
  priority: string
  dispute_type: string | null
  reason: string
  resolution_result: string | null
  created_at: string | null
}

export type AdminDisputeDetail = {
  id: number
  trade_id: string
  offer_id: string | null
  borrower_id: string | null
  lender_id: string | null
  raised_role: string
  dispute_type: string | null
  reason: string
  status: string
  priority: string
  resolution_result: string | null
  resolution_note: string | null
  created_at: string | null
  updated_at: string | null
  evidence: Array<{
    id: number
    uploaded_by_user_id: string
    uploaded_role: string
    evidence_type: string
    file_url: string | null
    text_note: string | null
    created_at: string | null
  }>
}

export type AdminManualReview = {
  id: number
  user_id: string | null
  trade_id: string | null
  offer_id: string | null
  reason: string
  risk_score: number
  status: string
  decision: string | null
  review_note: string | null
  created_at: string | null
}

export type AdminAnnouncement = {
  id: string
  lang: string
  title: string
  body: string
  link_url: string | null
  active: boolean
  starts_at: string | null
  ends_at: string | null
  created_at: string | null
}

export type AdminReportOverview = {
  range: { from: string; to: string }
  users: { total: number; new: number }
  offers: { total: number; new: number; pending: number }
  trades: { total: number; new: number; active: number; completed: number; failed: number }
  disputes: { open: number; new: number }
  risk: { pending_events: number; new_events: number }
}

export type AdminTrendSeries = {
  labels: string[]
  values: number[]
}

export type AdminReportTrends = {
  range: { from: string; to: string }
  users_new: AdminTrendSeries
  offers_new: AdminTrendSeries
  trades_new: AdminTrendSeries
  risk_events_new: AdminTrendSeries
  disputes_new: AdminTrendSeries
}

export type AdminConfigItem = {
  key: string
  value: Record<string, unknown>
  updated_at: string | null
}
