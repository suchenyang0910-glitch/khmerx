import { useEffect, useMemo, useState } from "react"
import { Link } from "react-router-dom"
import Card from "@/components/ui/Card"
import Badge from "@/components/ui/Badge"
import Button from "@/components/ui/Button"
import { apiV1 } from "@/api/client"
import { useAuthStore } from "@/stores/authStore"
import { Clock, ChevronRight } from "lucide-react"

type TradeListItemV1 = {
  id: string
  amount: number
  term_days: number
  rate_percent: number
  status: string
  lend_deadline?: string | null
}

function fmtCountdown(deadlineIso?: string | null) {
  if (!deadlineIso) return null
  const ms = new Date(deadlineIso).getTime() - Date.now()
  if (Number.isNaN(ms)) return null
  if (ms <= 0) return "00:00:00"
  const s = Math.floor(ms / 1000)
  const hh = String(Math.floor(s / 3600)).padStart(2, "0")
  const mm = String(Math.floor((s % 3600) / 60)).padStart(2, "0")
  const ss = String(s % 60).padStart(2, "0")
  return `${hh}:${mm}:${ss}`
}

function statusTone(status: string): "blue" | "green" | "yellow" | "red" | "zinc" {
  if (status === "completed") return "green"
  if (status === "matched" || status === "lend_confirmed" || status === "repayment_confirmed" || status === "repaying") return "blue"
  if (status === "dispute") return "yellow"
  if (status === "defaulted" || status === "cancelled") return "red"
  return "zinc"
}

export default function Trades() {
  const user = useAuthStore((s) => s.user)
  const [data, setData] = useState<{ as_borrower: TradeListItemV1[]; as_lender: TradeListItemV1[] } | null>(null)
  const [loading, setLoading] = useState(false)
  const [now, setNow] = useState(Date.now())

  useEffect(() => {
    const t = setInterval(() => setNow(Date.now()), 1000)
    return () => clearInterval(t)
  }, [])

  useEffect(() => {
    let cancelled = false
    const run = async () => {
      if (!user) return
      setLoading(true)
      try {
        const [a, b] = await Promise.all([
          apiV1.get<{ ok: boolean; data: TradeListItemV1[] }>("/trades", { params: { status: "active", role: "borrower" } }),
          apiV1.get<{ ok: boolean; data: TradeListItemV1[] }>("/trades", { params: { status: "active", role: "lender" } }),
        ])
        if (!cancelled) setData({ as_borrower: a.data.data || [], as_lender: b.data.data || [] })
      } finally {
        if (!cancelled) setLoading(false)
      }
    }
    run()
    return () => {
      cancelled = true
    }
  }, [user])

  const trades = useMemo(() => {
    const a = data?.as_borrower || []
    const b = data?.as_lender || []
    return [...a, ...b]
  }, [data])

  return (
    <div className="space-y-3">
      <div className="flex items-center justify-between">
        <div>
          <div className="text-sm font-semibold text-zinc-900">我的交易</div>
          <div className="text-xs text-zinc-500">查看状态、下一步与倒计时</div>
        </div>
        <Link to="/borrow"><Button size="sm">创建借款</Button></Link>
      </div>

      {loading ? (
        <div className="space-y-3">
          <div className="h-20 animate-pulse rounded-2xl bg-white" />
          <div className="h-20 animate-pulse rounded-2xl bg-white" />
        </div>
      ) : trades.length === 0 ? (
        <Card className="p-4">
          <div className="text-sm text-zinc-700">暂无交易记录</div>
          <div className="mt-1 text-xs text-zinc-500">先发布借款或去出借市场接单。</div>
        </Card>
      ) : (
        trades.map((t) => {
          const cd = fmtCountdown(t.lend_deadline)
          void now
          return (
            <Link key={t.id} to={`/trade/${t.id}`}>
              <Card className="p-4 hover:shadow-md transition-shadow">
                <div className="flex items-center justify-between">
                  <div className="text-base font-semibold text-zinc-900">${t.amount}</div>
                  <div className="flex items-center gap-2">
                    <Badge tone={statusTone(t.status)}>{t.status}</Badge>
                    <ChevronRight className="h-4 w-4 text-zinc-400" />
                  </div>
                </div>
                <div className="mt-1 text-xs text-zinc-500">{t.term_days} 天 · 费率 {t.rate_percent}%</div>
                {t.status === "matched" && cd ? (
                  <div className="mt-2 inline-flex items-center gap-2 rounded-xl bg-amber-50 px-3 py-2 text-sm text-amber-900">
                    <Clock className="h-4 w-4" />
                    <span>等待放款倒计时：{fmtCountdown(t.lend_deadline)}</span>
                  </div>
                ) : null}
              </Card>
            </Link>
          )
        })
      )}
    </div>
  )
}
