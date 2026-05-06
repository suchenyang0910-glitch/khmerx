import { useEffect, useState } from "react"
import { fetchTrades } from "@/api/admin"
import type { AdminTrade } from "@/api/types"
import { Card } from "@/components/ui/Card"

export default function Trades() {
  const [rows, setRows] = useState<AdminTrade[]>([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    let mounted = true
    setLoading(true)
    setError(null)
    fetchTrades({ limit: 50 })
      .then((d) => {
        if (mounted) setRows(d)
      })
      .catch(() => {
        if (mounted) setError("加载失败")
      })
      .finally(() => {
        if (mounted) setLoading(false)
      })
    return () => {
      mounted = false
    }
  }, [])

  return (
    <div>
      <div className="mb-5">
        <div className="text-xl font-semibold">交易</div>
        <div className="mt-1 text-sm text-zinc-400">P2P 交易列表</div>
      </div>

      {error ? <Card className="border-red-900 bg-red-950 text-red-200">{error}</Card> : null}

      <Card className="p-0">
        <div className="overflow-auto">
          <table className="min-w-[1100px] w-full text-left text-sm">
            <thead className="border-b border-zinc-800 text-zinc-400">
              <tr>
                <th className="px-4 py-3">trade_id</th>
                <th className="px-4 py-3">offer_id</th>
                <th className="px-4 py-3">borrower</th>
                <th className="px-4 py-3">lender</th>
                <th className="px-4 py-3">金额</th>
                <th className="px-4 py-3">状态</th>
                <th className="px-4 py-3">来源</th>
                <th className="px-4 py-3">创建时间</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-zinc-900">
              {loading ? (
                <tr>
                  <td className="px-4 py-6 text-zinc-400" colSpan={8}>
                    加载中...
                  </td>
                </tr>
              ) : rows.length === 0 ? (
                <tr>
                  <td className="px-4 py-6 text-zinc-400" colSpan={8}>
                    暂无数据
                  </td>
                </tr>
              ) : (
                rows.map((t) => (
                  <tr key={t.id} className="hover:bg-zinc-900/40">
                    <td className="px-4 py-3 font-mono text-xs">{t.id}</td>
                    <td className="px-4 py-3 font-mono text-xs">{t.offer_id}</td>
                    <td className="px-4 py-3 font-mono text-xs">{t.borrower_id}</td>
                    <td className="px-4 py-3 font-mono text-xs">{t.lender_id}</td>
                    <td className="px-4 py-3">${t.amount}</td>
                    <td className="px-4 py-3">{t.status}</td>
                    <td className="px-4 py-3">{t.fund_source}</td>
                    <td className="px-4 py-3 font-mono text-xs">{t.created_at ?? "-"}</td>
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

