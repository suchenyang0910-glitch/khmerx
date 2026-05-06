import { useEffect, useMemo, useState } from "react"
import { fetchDisputeDetail, fetchDisputes, resolveDispute } from "@/api/admin"
import type { AdminDispute, AdminDisputeDetail } from "@/api/types"
import { Card } from "@/components/ui/Card"
import { Button } from "@/components/ui/Button"

export default function Disputes() {
  const [status, setStatus] = useState("open")
  const [rows, setRows] = useState<AdminDispute[]>([])
  const [selectedId, setSelectedId] = useState<number | null>(null)
  const [detail, setDetail] = useState<AdminDisputeDetail | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [resolution, setResolution] = useState("manual_continue")
  const [note, setNote] = useState("")

  const canResolve = useMemo(() => Boolean(selectedId && resolution.trim()), [selectedId, resolution])

  async function reload() {
    setLoading(true)
    setError(null)
    try {
      setRows(await fetchDisputes({ status: status || undefined, limit: 100 }))
    } catch {
      setError("加载失败")
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    reload()
  }, [status])

  async function loadDetail(id: number) {
    setSelectedId(id)
    setDetail(null)
    setError(null)
    try {
      setDetail(await fetchDisputeDetail(id))
    } catch {
      setError("加载详情失败")
    }
  }

  return (
    <div>
      <div className="mb-5 flex flex-wrap items-end justify-between gap-3">
        <div>
          <div className="text-xl font-semibold">争议</div>
          <div className="mt-1 text-sm text-zinc-400">查看证据并做出裁决</div>
        </div>
        <div className="flex items-center gap-2">
          <select
            className="rounded-xl border border-zinc-800 bg-zinc-950 px-3 py-2 text-sm outline-none focus:border-blue-600"
            value={status}
            onChange={(e) => setStatus(e.target.value)}
          >
            <option value="open">open</option>
            <option value="reviewing">reviewing</option>
            <option value="resolved">resolved</option>
            <option value="">all</option>
          </select>
          <Button variant="secondary" onClick={reload} disabled={loading}>
            {loading ? "刷新中..." : "刷新"}
          </Button>
        </div>
      </div>

      {error ? <Card className="border-red-900 bg-red-950 text-red-200">{error}</Card> : null}

      <div className="grid gap-4 lg:grid-cols-2">
        <Card className="p-0">
          <div className="overflow-auto">
            <table className="min-w-[920px] w-full text-left text-sm">
              <thead className="border-b border-zinc-800 text-zinc-400">
                <tr>
                  <th className="px-4 py-3">id</th>
                  <th className="px-4 py-3">trade_id</th>
                  <th className="px-4 py-3">status</th>
                  <th className="px-4 py-3">priority</th>
                  <th className="px-4 py-3">type</th>
                  <th className="px-4 py-3">time</th>
                  <th className="px-4 py-3">action</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-zinc-900">
                {rows.length === 0 ? (
                  <tr>
                    <td className="px-4 py-6 text-zinc-400" colSpan={7}>
                      暂无数据
                    </td>
                  </tr>
                ) : (
                  rows.map((d) => (
                    <tr key={d.id} className="hover:bg-zinc-900/40">
                      <td className="px-4 py-3 font-mono text-xs">{d.id}</td>
                      <td className="px-4 py-3 font-mono text-xs">{d.trade_id}</td>
                      <td className="px-4 py-3">{d.status}</td>
                      <td className="px-4 py-3">{d.priority}</td>
                      <td className="px-4 py-3">{d.dispute_type ?? "-"}</td>
                      <td className="px-4 py-3 font-mono text-xs">{d.created_at ?? "-"}</td>
                      <td className="px-4 py-3">
                        <Button variant="secondary" onClick={() => loadDetail(d.id)}>
                          查看
                        </Button>
                      </td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>
        </Card>

        <Card>
          <div className="text-sm font-semibold">争议详情</div>
          {!detail ? (
            <div className="mt-3 text-sm text-zinc-400">选择左侧一条记录查看</div>
          ) : (
            <div className="mt-4 space-y-4">
              <div className="rounded-xl border border-zinc-800 bg-zinc-950 p-4">
                <div className="text-xs text-zinc-500">reason</div>
                <div className="mt-1 text-sm text-zinc-200">{detail.reason}</div>
              </div>
              <div>
                <div className="text-xs text-zinc-500">evidence</div>
                <div className="mt-2 space-y-2">
                  {detail.evidence.length === 0 ? (
                    <div className="text-sm text-zinc-400">无证据</div>
                  ) : (
                    detail.evidence.map((e) => (
                      <div key={e.id} className="rounded-xl border border-zinc-800 bg-zinc-950 p-3">
                        <div className="flex flex-wrap items-center justify-between gap-2 text-xs text-zinc-500">
                          <span>#{e.id} / {e.evidence_type}</span>
                          <span>{e.created_at ?? "-"}</span>
                        </div>
                        <div className="mt-2 text-sm text-zinc-200">{e.text_note ?? ""}</div>
                        {e.file_url ? (
                          <a className="mt-2 inline-block text-sm text-blue-400" href={e.file_url} target="_blank" rel="noreferrer">
                            打开文件
                          </a>
                        ) : null}
                      </div>
                    ))
                  )}
                </div>
              </div>

              <div className="grid gap-3 md:grid-cols-2">
                <div>
                  <div className="text-sm text-zinc-300">裁决结果</div>
                  <select
                    className="mt-2 w-full rounded-xl border border-zinc-800 bg-zinc-950 px-3 py-2 text-sm outline-none focus:border-blue-600"
                    value={resolution}
                    onChange={(e) => setResolution(e.target.value)}
                  >
                    <option value="borrower_win">borrower_win</option>
                    <option value="lender_win">lender_win</option>
                    <option value="both_fault">both_fault</option>
                    <option value="cancel_trade">cancel_trade</option>
                    <option value="manual_continue">manual_continue</option>
                    <option value="fraud">fraud</option>
                  </select>
                </div>
                <div>
                  <div className="text-sm text-zinc-300">备注</div>
                  <input
                    className="mt-2 w-full rounded-xl border border-zinc-800 bg-zinc-950 px-3 py-2 text-sm outline-none focus:border-blue-600"
                    value={note}
                    onChange={(e) => setNote(e.target.value)}
                    placeholder="可选"
                  />
                </div>
              </div>
              <Button
                disabled={!canResolve}
                onClick={async () => {
                  if (!selectedId) return
                  setError(null)
                  try {
                    await resolveDispute(selectedId, { resolution_result: resolution, resolution_note: note })
                    await reload()
                    await loadDetail(selectedId)
                  } catch {
                    setError("裁决失败")
                  }
                }}
              >
                提交裁决
              </Button>
            </div>
          )}
        </Card>
      </div>
    </div>
  )
}

