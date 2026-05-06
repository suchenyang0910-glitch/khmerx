import Card from "@/components/ui/Card"
import Badge from "@/components/ui/Badge"
import Button from "@/components/ui/Button"
import type { RepaymentScheduleItem } from "@/api/types"

export default function RepaymentPlan({
  role,
  schedules,
  onUpload,
  onConfirm,
}: {
  role: "borrower" | "lender" | "unknown"
  schedules: RepaymentScheduleItem[]
  onUpload: (period: number) => void
  onConfirm: (period: number) => void
}) {
  const soonDue = schedules.some((s) => {
    if (!s.due_at) return false
    const ms = new Date(s.due_at).getTime() - Date.now()
    return ms > 0 && ms <= 24 * 3600 * 1000 && (s.status === "pending" || s.status === "overdue")
  })

  return (
    <Card className="p-4">
      <div className="text-sm font-semibold text-zinc-900">还款计划</div>
      <div className="mt-2 space-y-2">
        {schedules.length === 0 ? (
          <div className="text-sm text-zinc-600">暂无还款计划</div>
        ) : (
          schedules.map((s) => (
            <div key={s.id} className="flex items-center justify-between rounded-2xl border border-zinc-100 bg-white px-3 py-2">
              <div>
                <div className="text-sm font-medium text-zinc-900">第 {s.period} 期 · ${Number(s.total).toFixed(2)}</div>
                <div className="text-xs text-zinc-500">到期：{s.due_at ? new Date(s.due_at).toLocaleString() : "-"}</div>
              </div>
              <div className="flex items-center gap-2">
                <Badge tone={s.status === "paid" ? "green" : s.status === "overdue" ? "red" : s.status === "paid_pending" ? "yellow" : "zinc"}>{s.status}</Badge>
                {role === "borrower" && (s.status === "pending" || s.status === "overdue") ? (
                  <Button size="sm" onClick={() => onUpload(s.period)}>上传</Button>
                ) : null}
                {role === "lender" && s.status === "paid_pending" ? (
                  <Button size="sm" onClick={() => onConfirm(s.period)}>确认</Button>
                ) : null}
              </div>
            </div>
          ))
        )}
      </div>

      {soonDue ? (
        <div className="mt-3 rounded-2xl bg-amber-50 p-3 text-sm text-amber-900">
          明天到期：请及时还款，逾期将影响信用与额度。
        </div>
      ) : null}
    </Card>
  )
}

