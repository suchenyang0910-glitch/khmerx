import { useEffect, useMemo, useState } from "react"
import { fetchUsers } from "@/api/admin"
import type { AdminUser } from "@/api/types"
import { Card } from "@/components/ui/Card"

export default function Users() {
  const [q, setQ] = useState("")
  const [rows, setRows] = useState<AdminUser[]>([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const canSearch = useMemo(() => q.trim().length === 0 || q.trim().length >= 2, [q])

  useEffect(() => {
    let mounted = true
    setLoading(true)
    setError(null)
    fetchUsers({ q: q.trim() || undefined, limit: 50 })
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
  }, [q])

  return (
    <div>
      <div className="mb-5 flex flex-wrap items-end justify-between gap-3">
        <div>
          <div className="text-xl font-semibold">用户</div>
          <div className="mt-1 text-sm text-zinc-400">按 TG ID 或昵称检索</div>
        </div>
        <div className="w-full max-w-md">
          <input
            className="w-full rounded-xl border border-zinc-800 bg-zinc-950 px-3 py-2 text-sm outline-none focus:border-blue-600"
            value={q}
            onChange={(e) => setQ(e.target.value)}
            placeholder="输入 tg_id 或昵称"
          />
          {!canSearch ? <div className="mt-1 text-xs text-zinc-500">至少输入 2 个字符</div> : null}
        </div>
      </div>

      {error ? <Card className="border-red-900 bg-red-950 text-red-200">{error}</Card> : null}

      <Card className="p-0">
        <div className="overflow-auto">
          <table className="min-w-[980px] w-full text-left text-sm">
            <thead className="border-b border-zinc-800 text-zinc-400">
              <tr>
                <th className="px-4 py-3">tg_id</th>
                <th className="px-4 py-3">昵称</th>
                <th className="px-4 py-3">角色</th>
                <th className="px-4 py-3">风险</th>
                <th className="px-4 py-3">信用分</th>
                <th className="px-4 py-3">手机号</th>
                <th className="px-4 py-3">ABA</th>
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
                rows.map((u) => (
                  <tr key={u.id} className="hover:bg-zinc-900/40">
                    <td className="px-4 py-3 font-mono text-xs">{u.tg_id}</td>
                    <td className="px-4 py-3">{u.name}</td>
                    <td className="px-4 py-3">{u.role}</td>
                    <td className="px-4 py-3">{u.risk_level}</td>
                    <td className="px-4 py-3">{u.credit_score}</td>
                    <td className="px-4 py-3">{u.phone ?? "-"}</td>
                    <td className="px-4 py-3">{u.aba_account ? `${u.aba_account} / ${u.aba_name ?? ""}` : "-"}</td>
                    <td className="px-4 py-3 font-mono text-xs">{u.created_at ?? "-"}</td>
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

