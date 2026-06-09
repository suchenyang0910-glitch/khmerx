export type Tab = 'orders' | 'factories' | 'collections'

export type FactoryRow = {
  id: string
  name: string
  industry?: string
  location: string
  owner_type?: string
  salary_cycle?: string
  worker_count?: number
  risk_level: string
  default_rate?: number
  hr_contact?: string
  is_active: boolean
  created_at?: string | null
}

export type OrderRow = {
  id: string
  user_id: string
  employment_id: string
  status: string
  principal: number
  fee: number
  interest: number
  total_due: number
  tenor_days: number
  due_date: string | null
  risk_score: number | null
  decision: string
  created_at: string | null
}

export type OrderDetail = {
  order: {
    id: string
    user_id: string
    employment_id: string
    status: string
    principal: number
    fee: number
    interest: number
    disbursement_amount: number
    tenor_days: number
    due_date: string | null
    risk_score: number | null
    decision: string
    decision_notes: string
    approved_by: string
    disbursed_by: string
    disbursed_at: string | null
    disbursement_ref: string
    created_at: string | null
  }
  employment: {
    id: string
    user_id: string
    factory_id: string
    employee_no: string
    pay_cycle: string
    pay_method: string
    verify_status: string
    verify_notes: string
    join_date: string | null
    salary_amount: number | null
    salary_pay_day: number | null
  } | null
  factory: {
    id: string
    name: string
    location: string
    risk_level: string
    is_active: boolean
  } | null
  proofs: Array<{
    id: string
    amount: number
    file_path: string
    note: string
    status: string
    created_at: string | null
  }>
  schedules: Array<{
    id: string
    installment_no: number
    due_date: string
    due_amount: number
    paid_amount: number
    status: string
  }>
  ledger: Array<{
    id: string
    event_type: string
    account: string
    dr_amount: number
    cr_amount: number
    external_ref: string
    created_at: string | null
  }>
  collection: {
    id: string
    dpd: number
    stage: string
    status: string
    assignee: string
    last_contact_at: string | null
    next_follow_up_at: string | null
    updated_at: string | null
  } | null
}

export type CollectionRow = {
  id: string
  order_id: string
  dpd: number
  stage: string
  status: string
  assignee: string
  last_contact_at: string | null
  next_follow_up_at: string | null
  updated_at: string | null
  principal: number
  total_due: number
  due_date: string | null
  order_status: string
  risk_score: number | null
  factory_name: string
  factory_risk_level: string
  employee_no: string
}

export type CollectionDetail = {
  case: {
    id: string
    order_id: string
    dpd: number
    stage: string
    status: string
    assignee: string
    last_contact_at: string | null
    next_follow_up_at: string | null
    updated_at: string | null
  }
  order: {
    id: string
    status: string
    principal: number
    fee: number
    interest: number
    total_due: number
    disbursement_amount: number
    due_date: string | null
    risk_score: number | null
  } | null
  employment: {
    id: string
    employee_no: string
    department: string
    position: string
    verify_status: string
    salary_amount: number | null
  } | null
  factory: {
    id: string
    name: string
    location: string
    risk_level: string
    hr_contact: string
  } | null
  events: Array<{
    id: string
    channel: string
    result: string
    reason_code: string
    note: string
    ptp_date: string | null
    ptp_amount: number
    actor: string
    created_at: string | null
  }>
}
