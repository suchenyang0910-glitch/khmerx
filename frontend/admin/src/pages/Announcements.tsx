import { useEffect, useState } from "react"
import { fetchAnnouncements, upsertAnnouncement } from "@/api/admin"
import type { AdminAnnouncement } from "@/api/types"
import { Card } from "@/components/ui/Card"
import { Button } from "@/components/ui/Button"

export default function Announcements() {
  const [rows, setRows] = useState<AdminAnnouncement[]>([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const [lang, setLang] = useState("km")
  const [title, setTitle] = useState("")
  const [body, setBody] = useState("")
  const [linkUrl, setLinkUrl] = useState("")
  const [active, setActive] = useState(true)

  async function reload() {
    setLoading(true)
    setError(null)
    try {
      setRows(await fetchAnnouncements({ lang: lang || undefined, limit: 100 }))
    } catch {
      setError("加载失败")
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    reload()
  }, [lang])

  return (
    <div>
      <div className="mb-5 flex flex-wrap items-end justify-between gap-3">
        <div>
          <div className="text-xl font-semibold">公告</div>
          <div className="mt-1 text-sm text-zinc-400">用于 Mini App 首页展示</div>
        </div>
        <div className="flex items-center gap-2">
          <select
            className="rounded-xl border border-zinc-800 bg-zinc-950 px-3 py-2 text-sm outline-none focus:border-blue-600"
            value={lang}
            onChange={(e) => setLang(e.target.value)}
          >
            <option value="km">km</option>
            <option value="zh">zh</option>
            <option value="en">en</option>
            <option value="">all</option>
          </select>
          <Button variant="secondary" onClick={reload} disabled={loading}>
            {loading ? "刷新中..." : "刷新"}
          </Button>
        </div>
      </div>

      {error ? <Card className="border-red-900 bg-red-950 text-red-200">{error}</Card> : null}

      <Card>
        <div className="grid gap-3 md:grid-cols-2">
          <div>
            <div className="text-sm text-zinc-300">标题</div>
            <input className="mt-2 w-full rounded-xl border border-zinc-800 bg-zinc-950 px-3 py-2 text-sm outline-none focus:border-blue-600" value={title} onChange={(e) => setTitle(e.target.value)} />
          </div>
          <div>
            <div className="text-sm text-zinc-300">跳转链接（可选）</div>
            <input className="mt-2 w-full rounded-xl border border-zinc-800 bg-zinc-950 px-3 py-2 text-sm outline-none focus:border-blue-600" value={linkUrl} onChange={(e) => setLinkUrl(e.target.value)} />
          </div>
          <div className="md:col-span-2">
            <div className="text-sm text-zinc-300">内容</div>
            <textarea
              className="mt-2 min-h-[88px] w-full rounded-xl border border-zinc-800 bg-zinc-950 px-3 py-2 text-sm outline-none focus:border-blue-600"
              value={body}
              onChange={(e) => setBody(e.target.value)}
            />
          </div>
        </div>
        <div className="mt-4 flex flex-wrap items-center gap-3">
          <label className="flex items-center gap-2 text-sm text-zinc-300">
            <input type="checkbox" checked={active} onChange={(e) => setActive(e.target.checked)} />
            active
          </label>
          <Button
            disabled={!title.trim() || !body.trim()}
            onClick={async () => {
              setError(null)
              try {
                await upsertAnnouncement({
                  lang: lang || "km",
                  title: title.trim(),
                  body: body.trim(),
                  link_url: linkUrl.trim() || null,
                  active,
                })
                setTitle("")
                setBody("")
                setLinkUrl("")
                await reload()
              } catch {
                setError("保存失败")
              }
            }}
          >
            发布公告
          </Button>
        </div>
      </Card>

      <div className="mt-4">
        <Card className="p-0">
          <div className="overflow-auto">
            <table className="min-w-[980px] w-full text-left text-sm">
              <thead className="border-b border-zinc-800 text-zinc-400">
                <tr>
                  <th className="px-4 py-3">time</th>
                  <th className="px-4 py-3">lang</th>
                  <th className="px-4 py-3">title</th>
                  <th className="px-4 py-3">body</th>
                  <th className="px-4 py-3">active</th>
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
                  rows.map((a) => (
                    <tr key={a.id} className="hover:bg-zinc-900/40">
                      <td className="px-4 py-3 font-mono text-xs">{a.created_at ?? "-"}</td>
                      <td className="px-4 py-3">{a.lang}</td>
                      <td className="px-4 py-3">{a.title}</td>
                      <td className="px-4 py-3 text-zinc-300">{a.body}</td>
                      <td className="px-4 py-3">{a.active ? "yes" : "no"}</td>
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

