import { adminApi } from "@/api/client"
import type {
  AdminDashboard,
  AdminDispute,
  AdminDisputeDetail,
  AdminFlaggedUser,
  AdminInterestRate,
  AdminManualReview,
  AdminRiskEvent,
  AdminRiskRule,
  AdminAnnouncement,
  AdminConfigItem,
  AdminReportOverview,
  AdminReportTrends,
  AdminNotification,
  AdminOffer,
  AdminTrade,
  AdminUser,
} from "@/api/types"

export async function adminLogin(input: { username: string; password: string }) {
  const res = await adminApi.post("/login", input, { headers: { Authorization: undefined } })
  return res.data as { token: string; expires_in: number; username: string }
}

export async function fetchDashboard() {
  const res = await adminApi.get("/dashboard")
  return res.data as AdminDashboard
}

export async function fetchUsers(params: { q?: string; limit?: number }) {
  const res = await adminApi.get("/users", { params })
  return res.data as AdminUser[]
}

export async function fetchOffers(params: { status?: string; limit?: number }) {
  const res = await adminApi.get("/offers", { params })
  return res.data as AdminOffer[]
}

export async function fetchTrades(params: { status?: string; limit?: number }) {
  const res = await adminApi.get("/trades", { params })
  return res.data as AdminTrade[]
}

export async function fetchNotifications(params: { user_id?: string; limit?: number }) {
  const res = await adminApi.get("/notifications", { params })
  return res.data as AdminNotification[]
}

export async function createNotification(input: {
  user_id: string
  type?: string
  title: string
  body: string
  target_type?: string | null
  target_id?: string | null
}) {
  const res = await adminApi.post("/notifications", input)
  return res.data as AdminNotification
}

export async function fetchInterestRates() {
  const res = await adminApi.get("/interest-rates")
  return res.data as AdminInterestRate[]
}

export async function upsertInterestRate(input: {
  term_days: number
  credit_level: string
  rate_percent: number
  mode?: string
  enabled?: boolean
}) {
  const res = await adminApi.post("/interest-rates", input)
  return res.data as AdminInterestRate
}

export async function fetchRiskDashboard() {
  const res = await adminApi.get("/risk/dashboard")
  return res.data as unknown
}

export async function fetchRiskEvents(params: { status?: string; limit?: number }) {
  const res = await adminApi.get("/risk/events", { params })
  return res.data as AdminRiskEvent[]
}

export async function markRiskEventHandled(eventId: number, handled_by: string) {
  const res = await adminApi.post(`/risk/events/${eventId}/handled`, { handled_by })
  return res.data as { id: number; status: string; handled_by: string; handled_at: string | null }
}

export async function fetchFlaggedUsers() {
  const res = await adminApi.get("/risk/flagged-users")
  return res.data as AdminFlaggedUser[]
}

export async function fetchRiskRules() {
  const res = await adminApi.get("/risk/rules")
  return res.data as AdminRiskRule[]
}

export async function upsertRiskRule(input: {
  code: string
  name: string
  rule_type: string
  threshold_value?: number | null
  action: string
  score_delta?: number
  enabled?: boolean
}) {
  const res = await adminApi.post("/risk/rules", input)
  return res.data as AdminRiskRule
}

export async function blockUser(userId: string, input: { reason?: string; hours?: number | null }) {
  const res = await adminApi.post(`/risk/users/${userId}/block`, input)
  return res.data as { ok: boolean }
}

export async function unblockUser(userId: string) {
  const res = await adminApi.post(`/risk/users/${userId}/unblock`)
  return res.data as { ok: boolean }
}

export async function adjustUserScore(userId: string, input: { score_delta: number; reason?: string }) {
  const res = await adminApi.post(`/risk/users/${userId}/score`, input)
  return res.data as { ok: boolean }
}

export async function fetchDisputes(params: { status?: string; limit?: number }) {
  const res = await adminApi.get("/disputes", { params })
  return res.data as AdminDispute[]
}

export async function fetchDisputeDetail(disputeId: number) {
  const res = await adminApi.get(`/disputes/${disputeId}`)
  return res.data as AdminDisputeDetail
}

export async function resolveDispute(disputeId: number, input: { resolution_result: string; resolution_note?: string }) {
  const res = await adminApi.post(`/disputes/${disputeId}/resolve`, input)
  return res.data as { id: number; status: string; resolution_result: string; resolution_note: string }
}

export async function fetchManualReviews(params: { status?: string; limit?: number }) {
  const res = await adminApi.get("/manual-reviews", { params })
  return res.data as AdminManualReview[]
}

export async function decideManualReview(caseId: number, input: { decision: string; review_note?: string }) {
  const res = await adminApi.post(`/manual-reviews/${caseId}/decide`, input)
  return res.data as { id: number; status: string; decision: string }
}

export async function fetchAnnouncements(params: { lang?: string; limit?: number }) {
  const res = await adminApi.get("/announcements", { params })
  return res.data as AdminAnnouncement[]
}

export async function upsertAnnouncement(input: {
  id?: string | null
  lang: string
  title: string
  body: string
  link_url?: string | null
  active?: boolean
}) {
  const res = await adminApi.post("/announcements", input)
  return res.data as AdminAnnouncement
}

export async function fetchReportOverview(params: { from_ymd?: string; to_ymd?: string }) {
  const res = await adminApi.get("/reports/overview", { params })
  return res.data as AdminReportOverview
}

export async function fetchReportTrends(params: { from_ymd?: string; to_ymd?: string }) {
  const res = await adminApi.get("/reports/trends", { params })
  return res.data as AdminReportTrends
}

export async function exportUsersCsv(params: { from_ymd?: string; to_ymd?: string }) {
  const res = await adminApi.get("/exports/users.csv", { params, responseType: "blob" })
  return res.data as Blob
}

export async function exportOrdersCsv(params: { from_ymd?: string; to_ymd?: string }) {
  const res = await adminApi.get("/exports/orders.csv", { params, responseType: "blob" })
  return res.data as Blob
}

export async function exportRiskEventsCsv(params: { from_ymd?: string; to_ymd?: string; status?: string }) {
  const res = await adminApi.get("/exports/risk-events.csv", { params, responseType: "blob" })
  return res.data as Blob
}

export async function fetchConfig() {
  const res = await adminApi.get("/config")
  return res.data as AdminConfigItem[]
}

export async function upsertConfig(input: { key: string; value: Record<string, unknown> }) {
  const res = await adminApi.post("/config", input)
  return res.data as AdminConfigItem
}
