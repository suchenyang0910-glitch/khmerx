import { useEffect, useState } from "react"
import { fetchDashboard } from "@/api/admin"
import type { AdminDashboard } from "@/api/types"
import { Card } from "@/components/ui/Card"

export default function Dashboard() {
  const [data, setData] = useState<AdminDashboard | null>(null)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    let mounted = true
    fetchDashboard()
      .then((d) => {
        if (mounted) setData(d)
      })
      .catch(() => {
        if (mounted) setError("加载失败")
      })
    return () => {
      mounted = false
    }
  }, [])

  return (
    <div>
      <div className="mb-5">
        <div className="text-xl font-semibold">仪表盘</div>
        <div className="mt-1 text-sm text-zinc-400">核心指标概览</div>
      </div>

      {error ? <Card className="border-red-900 bg-red-950 text-red-200">{error}</Card> : null}
      {!data ? (
        <div className="grid gap-4 md:grid-cols-4">
          {Array.from({ length: 4 }).map((_, i) => (
            <div key={i} className="h-24 animate-pulse rounded-2xl border border-zinc-800 bg-zinc-900/40" />
          ))}
        </div>
      ) : (
        <div className="grid gap-4 md:grid-cols-4">
          <Card>
            <div className="text-sm text-zinc-400">用户总数</div>
            <div className="mt-2 text-3xl font-semibold">{data.users}</div>
          </Card>
          <Card>
            <div className="text-sm text-zinc-400">待匹配挂单</div>
            <div className="mt-2 text-3xl font-semibold">{data.offers.pending}</div>
          </Card>
          <Card>
            <div className="text-sm text-zinc-400">进行中交易</div>
            <div className="mt-2 text-3xl font-semibold">{data.trades.active}</div>
          </Card>
          <Card>
            <div className="text-sm text-zinc-400">待处理风控事件</div>
            <div className="mt-2 text-3xl font-semibold">{data.risk.pending_events}</div>
          </Card>
        </div>
      )}
    </div>
  )
}

