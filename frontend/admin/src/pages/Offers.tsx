import { useEffect, useState } from "react"
import { fetchOffers } from "@/api/admin"
import type { AdminOffer } from "@/api/types"
import { Card } from "@/components/ui/Card"

export default function Offers() {
  const [rows, setRows] = useState<AdminOffer[]>([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    let mounted = true
    setLoading(true)
    setError(null)
    fetchOffers({ limit: 50 })
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
        <div className="text-xl font-semibold">挂单</div>
        <div className="mt-1 text-sm text-zinc-400">P2P 借款人挂单列表</div>
      </div>

      {error ? <Card className="border-red-900 bg-red-950 text-red-200">{error}</Card> : null}

      <Card className="p-0">
        <div className="overflow-auto">
          <table className="min-w-[980px] w-full text-left text-sm">
            <thead className="border-b border-zinc-800 text-zinc-400">
              <tr>
                <th className="px-4 py-3">offer_id</th>
                <th className="px-4 py-3">borrower_id</th>
                <th className="px-4 py-3">金额</th>
                <th className="px-4 py-3">期限</th>
                <th className="px-4 py-3">费</th>
                <th className="px-4 py-3">状态</th>
                <th className="px-4 py-3">创建时间</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-zinc-900">
              {loading ? (
                <tr>
                  <td className="px-4 py-6 text-zinc-400" colSpan={7}>
                    加载中...
                  </td>
                </tr>
              ) : rows.length === 0 ? (
                <tr>
                  <td className="px-4 py-6 text-zinc-400" colSpan={7}>
                    暂无数据
                  </td>
                </tr>
              ) : (
                rows.map((o) => (
                  <tr key={o.id} className="hover:bg-zinc-900/40">
                    <td className="px-4 py-3 font-mono text-xs">{o.id}</td>
                    <td className="px-4 py-3 font-mono text-xs">{o.borrower_id}</td>
                    <td className="px-4 py-3">${o.amount}</td>
                    <td className="px-4 py-3">{o.term_days}d</td>
                    <td className="px-4 py-3">${o.fee}</td>
                    <td className="px-4 py-3">{o.status}</td>
                    <td className="px-4 py-3 font-mono text-xs">{o.created_at ?? "-"}</td>
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

