import { useEffect, useState } from "react"
import { createNotification, fetchNotifications } from "@/api/admin"
import type { AdminNotification } from "@/api/types"
import { Button } from "@/components/ui/Button"
import { Card } from "@/components/ui/Card"

export default function Notifications() {
  const [userId, setUserId] = useState("")
  const [title, setTitle] = useState("")
  const [body, setBody] = useState("")
  const [rows, setRows] = useState<AdminNotification[]>([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [creating, setCreating] = useState(false)

  async function reload() {
    setLoading(true)
    setError(null)
    try {
      const res = await fetchNotifications({ user_id: userId.trim() || undefined, limit: 50 })
      setRows(res)
    } catch {
      setError("加载失败")
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    reload()
  }, [])

  return (
    <div>
      <div className="mb-5">
        <div className="text-xl font-semibold">通知</div>
        <div className="mt-1 text-sm text-zinc-400">给指定用户下发 App 内通知</div>
      </div>

      <Card>
        <div className="grid gap-3 md:grid-cols-3">
          <div className="md:col-span-1">
            <div className="text-sm text-zinc-300">user_id (UUID)</div>
            <input
              className="mt-2 w-full rounded-xl border border-zinc-800 bg-zinc-950 px-3 py-2 text-sm outline-none focus:border-blue-600"
              value={userId}
              onChange={(e) => setUserId(e.target.value)}
              placeholder="例如：8b9d..."
            />
          </div>
          <div className="md:col-span-1">
            <div className="text-sm text-zinc-300">标题</div>
            <input
              className="mt-2 w-full rounded-xl border border-zinc-800 bg-zinc-950 px-3 py-2 text-sm outline-none focus:border-blue-600"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              placeholder="例如：还款提醒"
            />
          </div>
          <div className="md:col-span-1">
            <div className="text-sm text-zinc-300">内容</div>
            <input
              className="mt-2 w-full rounded-xl border border-zinc-800 bg-zinc-950 px-3 py-2 text-sm outline-none focus:border-blue-600"
              value={body}
              onChange={(e) => setBody(e.target.value)}
              placeholder="例如：明天到期，请按时还款"
            />
          </div>
        </div>
        <div className="mt-4 flex flex-wrap gap-3">
          <Button
            disabled={creating || !userId.trim() || !title.trim() || !body.trim()}
            onClick={async () => {
              setCreating(true)
              setError(null)
              try {
                await createNotification({ user_id: userId.trim(), title: title.trim(), body: body.trim() })
                setTitle("")
                setBody("")
                await reload()
              } catch {
                setError("创建失败")
              } finally {
                setCreating(false)
              }
            }}
          >
            {creating ? "发送中..." : "发送通知"}
          </Button>
          <Button variant="secondary" onClick={reload} disabled={loading}>
            {loading ? "刷新中..." : "刷新"}
          </Button>
        </div>
        {error ? <div className="mt-4 rounded-xl border border-red-900 bg-red-950 px-3 py-2 text-sm text-red-200">{error}</div> : null}
      </Card>

      <div className="mt-4">
        <Card className="p-0">
          <div className="overflow-auto">
            <table className="min-w-[980px] w-full text-left text-sm">
              <thead className="border-b border-zinc-800 text-zinc-400">
                <tr>
                  <th className="px-4 py-3">time</th>
                  <th className="px-4 py-3">user_id</th>
                  <th className="px-4 py-3">title</th>
                  <th className="px-4 py-3">body</th>
                  <th className="px-4 py-3">read</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-zinc-900">
                {rows.length === 0 ? (
                  <tr>
                    <td className="px-4 py-6 text-zinc-400" colSpan={5}>
                      暂无数据
                    </td>
                  </tr>
                ) : (
                  rows.map((n) => (
                    <tr key={n.id} className="hover:bg-zinc-900/40">
                      <td className="px-4 py-3 font-mono text-xs">{n.created_at ?? "-"}</td>
                      <td className="px-4 py-3 font-mono text-xs">{n.user_id}</td>
                      <td className="px-4 py-3">{n.title}</td>
                      <td className="px-4 py-3 text-zinc-300">{n.body}</td>
                      <td className="px-4 py-3">{n.read ? "yes" : "no"}</td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>
        </Card>
      </div>
    </div>
  )
}

