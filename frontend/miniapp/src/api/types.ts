export type RiskLevel = "normal" | "watch" | "flagged" | "restricted" | "blocked"

export type P2POfferStatus = "pending" | "matched" | "cancelled" | "expired"

export type P2PTradeStatus =
  | "matched"
  | "lend_confirmed"
  | "repayment_confirmed"
  | "repaying"
  | "completed"
  | "cancelled"
  | "defaulted"
  | "dispute"

export interface AppUser {
  id: string
  global_user_id?: string
  tg_id: number
  name: string
  photo_url?: string
  role: string
  language?: "km" | "cn" | "en"
  risk_level: string
  credit_score: number
  verification_level: string
  phone?: string
  phone_verified?: boolean
  aba_account?: string
  aba_name?: string
  total_borrowed?: number
  total_repaid?: number
  active_loans?: number
  profile_completed?: boolean
  credit_level?: string
  max_borrow_amount?: number
  active_trades?: number
  created_at: string
}

export interface UserRiskProfile {
  user_id: string
  risk_level: RiskLevel
  credit_score: number
  credit_level: "A" | "B" | "C" | "D" | "E"
  max_borrow_amount: number
  max_active_trades: number
  cancel_count: number
  matched_cancel_count: number
  overdue_count: number
  default_count: number
  dispute_lost_count: number
  is_blocked: boolean
  blocked_until?: string | null
  block_reason?: string | null
  updated_at?: string
}

export interface LoanCalcResult {
  principal: number
  term_days: number
  rate_percent: number
  interest: number
  received_amount: number
  repay_amount: number
  real_rate_percent: number
  apr_percent: number
}

export interface P2POffer {
  id: string
  borrower_id: string
  borrower_name?: string
  amount: number
  term_days: number
  rate: number
  fee: number
  total_amount: number
  status: P2POfferStatus
  created_at: string
  note?: string
}

export interface P2PTrade {
  id: string
  offer_id: string
  borrower_id: string
  lender_id: string
  amount: number
  term_days: number
  rate: number
  fee: number
  fee_status?: string
  total_repayable?: number
  status: P2PTradeStatus
  proof_url_from_lender?: string
  proof_url_from_borrower?: string
  advance_pay_deadline?: string | null
  created_at: string
  updated_at?: string
}

export interface RepaymentScheduleItem {
  id: string
  period: number
  due_at?: string | null
  principal: number
  interest: number
  total: number
  status: "pending" | "paid_pending" | "paid" | "overdue"
  paid_at?: string | null
  proof_url?: string
}

export interface Dispute {
  id: number
  trade_id: string
  status: string
  dispute_type: string
  reason: string
  created_at: string
}

export interface Notification {
  id: string
  type: string
  title: string
  body: string
  target_type?: string | null
  target_id?: string | null
  read: boolean
  created_at: string | null
}

export interface Announcement {
  id: string
  lang: string
  title: string
  body: string
  link_url: string | null
  created_at: string | null
}
