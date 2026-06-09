import { apiV1 } from "@/api/client"
import type {
  Announcement,
  CreditDetail,
  FinanceApplication,
  FinanceBizType,
  Notification,
  SalaryFactory,
  SalaryLoanOrder,
  SalaryLoanOrderDetail,
  SalaryLoanQuote,
  SalaryLoanUploadProofResult,
  UnifiedOrder,
} from "@/api/types"

export async function updatePreferredLanguage(lang: "km" | "cn" | "en") {
  const res = await apiV1.patch<{ ok: boolean; data: { profile_completed: boolean } }>("/me/profile", { language: lang })
  return res.data.data
}

export async function fetchAnnouncements() {
  const res = await apiV1.get<{ ok: boolean; data: Announcement[] }>("/announcements")
  return res.data.data
}

export async function fetchNotifications() {
  const res = await apiV1.get<{ ok: boolean; data: Notification[] }>("/notifications")
  return res.data.data
}

export async function markNotificationRead(notificationId: string) {
  const res = await apiV1.post<{ ok: boolean; data: { id: string; read: boolean } }>(`/notifications/${notificationId}/read`)
  return res.data.data
}

export type NotificationSettings = {
  repayment_reminders: boolean
  dispute_updates: boolean
}

export async function fetchNotificationSettings() {
  const res = await apiV1.get<{ ok: boolean; data: NotificationSettings }>("/notifications/settings")
  return res.data.data
}

export async function updateNotificationSettings(input: Partial<NotificationSettings>) {
  const res = await apiV1.put<{ ok: boolean; data: NotificationSettings }>("/notifications/settings", input)
  return res.data.data
}

export async function createFinanceApplication(input: { biz_type: FinanceBizType; payload: Record<string, unknown> }) {
  const res = await apiV1.post<{ ok: boolean; data: FinanceApplication }>("/applications", input)
  return res.data.data
}

export async function fetchMyApplications(params?: { biz_type?: string; status?: string; limit?: number; offset?: number }) {
  const res = await apiV1.get<{ ok: boolean; data: FinanceApplication[] }>("/applications", { params })
  return res.data.data
}

export async function fetchApplicationDetail(applicationId: string) {
  const res = await apiV1.get<{ ok: boolean; data: FinanceApplication }>(`/applications/${applicationId}`)
  return res.data.data
}

export async function fetchMyOrders(params?: { business_type?: string; status?: string; limit?: number; offset?: number }) {
  const res = await apiV1.get<{ ok: boolean; data: UnifiedOrder[] }>("/orders", { params })
  return res.data.data
}

export async function fetchSalaryFactories() {
  const res = await apiV1.get<{ ok: boolean; data: SalaryFactory[] }>("/salary-loan/factories")
  return res.data.data
}

export async function createSalaryEmployment(input: {
  factory_id: string
  employee_no?: string
  department?: string
  position?: string
  join_date?: string | null
  salary_amount?: number | null
  salary_pay_day?: number | null
  pay_cycle: "monthly" | "biweekly" | "daily"
  pay_method: "transfer" | "cash"
}) {
  const res = await apiV1.post<{ ok: boolean; data: { id: string } }>("/salary-loan/employment", input)
  return res.data.data
}

export async function createSalaryLoanOrder(input: { employment_id: string; principal: number; tenor_days: number; note?: string }) {
  const res = await apiV1.post<{ ok: boolean; data: SalaryLoanOrder }>("/salary-loan/orders", input)
  return res.data.data
}

export async function calculateSalaryLoanQuote(input: {
  factory_id: string
  principal: number
  tenor_days: number
  join_date?: string | null
  salary_amount?: number | null
  salary_pay_day?: number | null
  pay_cycle: "monthly" | "biweekly" | "daily"
  pay_method: "transfer" | "cash"
}) {
  const res = await apiV1.post<{ ok: boolean; data: SalaryLoanQuote }>("/salary-loan/calculate", input)
  return res.data.data
}

export async function fetchSalaryLoanOrderDetail(orderId: string) {
  const res = await apiV1.get<{ ok: boolean; data: SalaryLoanOrderDetail }>(`/salary-loan/orders/${orderId}`)
  return res.data.data
}

export async function uploadSalaryLoanRepaymentProof(orderId: string, input: { amount: number; note?: string; file: File }) {
  const form = new FormData()
  form.append("file", input.file)
  const res = await apiV1.post<{ ok: boolean; data: SalaryLoanUploadProofResult }>(
    `/salary-loan/orders/${orderId}/repayment-proof`,
    form,
    {
      params: { amount: input.amount, note: input.note || "" },
      headers: { "Content-Type": "multipart/form-data" },
    },
  )
  return res.data.data
}

export async function fetchMyCredit() {
  const res = await apiV1.get<{ ok: boolean; data: CreditDetail }>("/me/credit")
  return res.data.data
}
