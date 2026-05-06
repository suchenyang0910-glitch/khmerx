import { useEffect, useMemo, useState } from "react"
import {
  exportOrdersCsv,
  exportRiskEventsCsv,
  exportUsersCsv,
  fetchReportOverview,
  fetchReportTrends,
} from "@/api/admin"
import type { AdminReportOverview, AdminReportTrends } from "@/api/types"
import { Card } from "@/components/ui/Card"
import { Button } from "@/components/ui/Button"
import Sparkline from "@/components/charts/Sparkline"

function toYmd(d: Date) {
  const y = d.getFullYear()
  const m = String(d.getMonth() + 1).padStart(2, "0")
  const day = String(d.getDate()).padStart(2, "0")
  return `${y}-${m}-${day}`
}

function downloadBlob(blob: Blob, filename: string) {
  const url = URL.createObjectURL(blob)
  const a = document.createElement("a")
  a.href = url
  a.download = filename
  document.body.appendChild(a)
  a.click()
  a.remove()
  URL.revokeObjectURL(url)
}

export default function Reports() {
  const today = useMemo(() => {
    const now = new Date()
    return new Date(now.getFullYear(), now.getMonth(), now.getDate())
  }, [])
  const defaultFrom = useMemo(() => {
    const d = new Date(today)
    d.setDate(d.getDate() - 13)
    return d
  }, [today])

  const [fromYmd, setFromYmd] = useState(toYmd(defaultFrom))
  const [toYmdStr, setToYmdStr] = useState(toYmd(today))
  const [overview, setOverview] = useState<AdminReportOverview | null>(null)
  const [trends, setTrends] = useState<AdminReportTrends | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  async function reload() {
    setLoading(true)
    setError(null)
    try {
      const [o, t] = await Promise.all([
        fetchReportOverview({ from_ymd: fromYmd, to_ymd: toYmdStr }),
        fetchReportTrends({ from_ymd: fromYmd, to_ymd: toYmdStr }),
      ])
      setOverview(o)
      setTrends(t)
    } catch {
      setError("加载失败")
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    reload()
  }, [])

  const series = useMemo(() => {
    if (!trends) return []
    return [
      { label: "新增用户", s: trends.users_new, color: "#22c55e" },
      { label: "新增挂单", s: trends.offers_new, color: "#3b82f6" },
      { label: "新增订单", s: trends.trades_new, color: "#a855f7" },
      { label: "风险事件", s: trends.risk_events_new, color: "#f97316" },
      { label: "争议新增", s: trends.disputes_new, color: "#ef4444" },
    ]
  }, [trends])

  return (
    <div>
      <div className="mb-5 flex flex-wrap items-end justify-between gap-3">
        <div>
          <div className="text-xl font-semibold">报表总览</div>
          <div className="mt-1 text-sm text-zinc-400">核心指标与趋势</div>
        </div>
        <div className="flex flex-wrap items-center gap-2">
          <div className="flex items-center gap-2">
            <input
              type="date"
              className="rounded-xl border border-zinc-800 bg-zinc-950 px-3 py-2 text-sm outline-none focus:border-blue-600"
              value={fromYmd}
              onChange={(e) => setFromYmd(e.target.value)}
            />
            <span className="text-sm text-zinc-500">~</span>
            <input
              type="date"
              className="rounded-xl border border-zinc-800 bg-zinc-950 px-3 py-2 text-sm outline-none focus:border-blue-600"
              value={toYmdStr}
              onChange={(e) => setToYmdStr(e.target.value)}
            />
          </div>
          <Button onClick={reload} disabled={loading}>
            {loading ? "加载中..." : "查询"}
          </Button>
        </div>
      </div>

      {error ? <Card className="border-red-900 bg-red-950 text-red-200">{error}</Card> : null}

      {!overview ? (
        <div className="grid gap-4 md:grid-cols-4">
          {Array.from({ length: 8 }).map((_, i) => (
            <div key={i} className="h-24 animate-pulse rounded-2xl border border-zinc-800 bg-zinc-900/40" />
          ))}
        </div>
      ) : (
        <div className="grid gap-4 md:grid-cols-4">
          <Card>
            <div className="text-sm text-zinc-400">用户总数</div>
            <div className="mt-2 text-3xl font-semibold">{overview.users.total}</div>
            <div className="mt-2 text-sm text-zinc-500">区间新增 {overview.users.new}</div>
          </Card>
          <Card>
            <div className="text-sm text-zinc-400">挂单</div>
            <div className="mt-2 text-3xl font-semibold">{overview.offers.total}</div>
            <div className="mt-2 text-sm text-zinc-500">新增 {overview.offers.new} / 待匹配 {overview.offers.pending}</div>
          </Card>
          <Card>
            <div className="text-sm text-zinc-400">订单</div>
            <div className="mt-2 text-3xl font-semibold">{overview.trades.total}</div>
            <div className="mt-2 text-sm text-zinc-500">新增 {overview.trades.new} / 进行中 {overview.trades.active}</div>
          </Card>
          <Card>
            <div className="text-sm text-zinc-400">成功/失败</div>
            <div className="mt-2 text-3xl font-semibold">{overview.trades.completed}</div>
            <div className="mt-2 text-sm text-zinc-500">失败 {overview.trades.failed}</div>
          </Card>
          <Card>
            <div className="text-sm text-zinc-400">待处理风险事件</div>
            <div className="mt-2 text-3xl font-semibold">{overview.risk.pending_events}</div>
            <div className="mt-2 text-sm text-zinc-500">区间新增 {overview.risk.new_events}</div>
          </Card>
          <Card>
            <div className="text-sm text-zinc-400">争议</div>
            <div className="mt-2 text-3xl font-semibold">{overview.disputes.open}</div>
            <div className="mt-2 text-sm text-zinc-500">区间新增 {overview.disputes.new}</div>
          </Card>
          <Card className="md:col-span-2">
            <div className="text-sm text-zinc-400">数据区间</div>
            <div className="mt-2 text-lg font-semibold">{overview.range.from} ~ {overview.range.to}</div>
            <div className="mt-2 text-sm text-zinc-500">趋势图与导出均按此区间</div>
          </Card>
        </div>
      )}

      {trends ? (
        <div className="mt-4 grid gap-4 md:grid-cols-5">
          {series.map((item) => (
            <Card key={item.label}>
              <div className="flex items-start justify-between gap-3">
                <div>
                  <div className="text-sm text-zinc-400">{item.label}</div>
                  <div className="mt-2 text-2xl font-semibold">{item.s.values.reduce((a, b) => a + b, 0)}</div>
                </div>
                <Sparkline values={item.s.values} stroke={item.color} />
              </div>
              <div className="mt-2 text-xs text-zinc-500">{item.s.labels[0]} ~ {item.s.labels[item.s.labels.length - 1]}</div>
            </Card>
          ))}
        </div>
      ) : null}

      <div className="mt-6">
        <div className="mb-3 text-sm font-semibold text-zinc-200">CSV 导出</div>
        <div className="grid gap-3 md:grid-cols-3">
          <Card>
            <div className="text-sm text-zinc-400">用户</div>
            <div className="mt-3">
              <Button
                variant="secondary"
                onClick={async () => {
                  const blob = await exportUsersCsv({ from_ymd: fromYmd, to_ymd: toYmdStr })
                  downloadBlob(blob, `users_${fromYmd}_${toYmdStr}.csv`)
                }}
              >
                下载 CSV
              </Button>
            </div>
          </Card>
          <Card>
            <div className="text-sm text-zinc-400">订单（交易）</div>
            <div className="mt-3">
              <Button
                variant="secondary"
                onClick={async () => {
                  const blob = await exportOrdersCsv({ from_ymd: fromYmd, to_ymd: toYmdStr })
                  downloadBlob(blob, `orders_${fromYmd}_${toYmdStr}.csv`)
                }}
              >
                下载 CSV
              </Button>
            </div>
          </Card>
          <Card>
            <div className="text-sm text-zinc-400">风控事件</div>
            <div className="mt-3">
              <Button
                variant="secondary"
                onClick={async () => {
                  const blob = await exportRiskEventsCsv({ from_ymd: fromYmd, to_ymd: toYmdStr })
                  downloadBlob(blob, `risk_events_${fromYmd}_${toYmdStr}.csv`)
                }}
              >
                下载 CSV
              </Button>
            </div>
          </Card>
        </div>
      </div>
    </div>
  )
}

