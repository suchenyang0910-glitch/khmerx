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

export type FinanceBizType = "lease" | "installment" | "pledge"

export type FinanceApplicationStatus =
  | "draft"
  | "submitted"
  | "under_review"
  | "need_more_info"
  | "approved"
  | "rejected"
  | "canceled"

export interface FinanceApplication {
  id: string
  user_id: string
  biz_type: FinanceBizType
  status: FinanceApplicationStatus | string
  payload: Record<string, unknown>
  created_at?: string | null
  updated_at?: string | null
}

export type BusinessType = "loan" | "salary" | "rental" | "installment" | "pawn"

export type UnifiedOrderSourceType = "p2p_offer" | "p2p_trade" | "finance_application" | "salary_loan"

export interface UnifiedOrder {
  id: string
  business_type: BusinessType
  source_type: UnifiedOrderSourceType
  source_id: string
  status: string
  principal: number
  interest: number
  total_due: number
  due_at?: string | null
  created_at?: string | null
}

export type SalaryFactory = {
  id: string
  name: string
  industry: string
  location: string
  owner_type: string
  salary_cycle: string
  risk_level: string
  default_rate: number
}

export type SalaryEmployment = {
  id: string
  user_id: string
  factory_id: string
  employee_no: string
  department: string
  position: string
  join_date: string | null
  salary_amount: number | null
  salary_pay_day: number | null
  pay_cycle: "monthly" | "biweekly" | "daily"
  pay_method: "transfer" | "cash"
  verify_status: string
  verify_notes: string
  verified_at: string | null
  created_at: string | null
}

export type SalaryLoanOrder = {
  id: string
  user_id: string
  employment_id: string
  status: string
  currency: string
  principal: number
  fee: number
  interest: number
  disbursement_amount: number
  tenor_days: number
  due_date: string | null
  risk_score: number | null
  decision: string
  decision_notes: string
  created_at: string | null
  updated_at: string | null
}

export type SalaryLoanRepaymentSchedule = {
  id: string
  order_id: string
  installment_no: number
  due_date: string
  due_amount: number
  paid_amount: number
  status: string
  paid_at: string | null
}

export type SalaryLoanOrderDetail = {
  order: SalaryLoanOrder
  employment: SalaryEmployment
  factory: SalaryFactory | null
  schedules: SalaryLoanRepaymentSchedule[]
}

export type SalaryLoanQuote = {
  principal: number
  tenor_days: number
  risk_score: number
  reasons: string[]
  fee_rate: number
  interest_rate: number
  fee: number
  interest: number
  disbursement_amount: number
  total_due: number
  note: string
}

export type SalaryLoanUploadProofResult = {
  proof_id: string
  url: string
}

export interface CreditDetail {
  credit_score: number
  credit_level: string
  risk_level: string
  max_borrow_amount: number
  reasons: string[]
  logs: Array<{
    event_type: string
    risk_action: string
    score_change: number
    old_score: number
    new_score: number
    old_risk_level: string
    new_risk_level: string
    reason: string
    created_at?: string | null
  }>
}

export interface Product {
  id: string
  title: string
  description: string
  price: number
  status: string
  owner_id: string
  source: string
  is_verified: boolean
  images: string
  video_url: string
  contact_info: string
  category: string
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
