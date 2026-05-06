import { useEffect, useMemo, useState } from "react"
import { fetchRiskEvents, markRiskEventHandled } from "@/api/admin"
import type { AdminRiskEvent } from "@/api/types"
import { Card } from "@/components/ui/Card"
import { Button } from "@/components/ui/Button"

export default function RiskEvents() {
  const [status, setStatus] = useState<string>("pending")
  const [rows, setRows] = useState<AdminRiskEvent[]>([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const badge = useMemo(() => {
    return (sev: string) => {
      const s = sev.toLowerCase()
      return s === "high" ? "bg-red-950 text-red-200" : s === "medium" ? "bg-yellow-950 text-yellow-200" : "bg-zinc-800 text-zinc-200"
    }
  }, [])

  async function reload() {
    setLoading(true)
    setError(null)
    try {
      const data = await fetchRiskEvents({ status: status || undefined, limit: 100 })
      setRows(data)
    } catch {
      setError("加载失败")
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    reload()
  }, [status])

  return (
    <div>
      <div className="mb-5 flex flex-wrap items-end justify-between gap-3">
        <div>
          <div className="text-xl font-semibold">风控事件</div>
          <div className="mt-1 text-sm text-zinc-400">查看并处置风险事件</div>
        </div>
        <div className="flex items-center gap-2">
          <select
            className="rounded-xl border border-zinc-800 bg-zinc-950 px-3 py-2 text-sm outline-none focus:border-blue-600"
            value={status}
            onChange={(e) => setStatus(e.target.value)}
          >
            <option value="pending">pending</option>
            <option value="handled">handled</option>
            <option value="">all</option>
          </select>
          <Button variant="secondary" onClick={reload} disabled={loading}>
            {loading ? "刷新中..." : "刷新"}
          </Button>
        </div>
      </div>

      {error ? <Card className="border-red-900 bg-red-950 text-red-200">{error}</Card> : null}

      <Card className="p-0">
        <div className="overflow-auto">
          <table className="min-w-[1100px] w-full text-left text-sm">
            <thead className="border-b border-zinc-800 text-zinc-400">
              <tr>
                <th className="px-4 py-3">id</th>
                <th className="px-4 py-3">type</th>
                <th className="px-4 py-3">severity</th>
                <th className="px-4 py-3">status</th>
                <th className="px-4 py-3">user_id</th>
                <th className="px-4 py-3">trade_id</th>
                <th className="px-4 py-3">time</th>
                <th className="px-4 py-3">action</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-zinc-900">
              {rows.length === 0 ? (
                <tr>
                  <td className="px-4 py-6 text-zinc-400" colSpan={8}>
                    暂无数据
                  </td>
                </tr>
              ) : (
                rows.map((e) => (
                  <tr key={e.id} className="hover:bg-zinc-900/40">
                    <td className="px-4 py-3 font-mono text-xs">{e.id}</td>
                    <td className="px-4 py-3">{e.event_type}</td>
                    <td className="px-4 py-3">
                      <span className={`rounded-full px-2 py-1 text-xs ${badge(e.severity)}`}>{e.severity}</span>
                    </td>
                    <td className="px-4 py-3">{e.status}</td>
                    <td className="px-4 py-3 font-mono text-xs">{e.user_id ?? "-"}</td>
                    <td className="px-4 py-3 font-mono text-xs">{e.trade_id ?? "-"}</td>
                    <td className="px-4 py-3 font-mono text-xs">{e.created_at ?? "-"}</td>
                    <td className="px-4 py-3">
                      {e.status === "pending" ? (
                        <Button
                          variant="secondary"
                          onClick={async () => {
                            await markRiskEventHandled(e.id, "admin")
                            await reload()
                          }}
                        >
                          标记已处理
                        </Button>
                      ) : (
                        <span className="text-xs text-zinc-500">{e.handled_at ? `handled@${e.handled_at}` : "-"}</span>
                      )}
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </Card>
    </div>
  )
}

