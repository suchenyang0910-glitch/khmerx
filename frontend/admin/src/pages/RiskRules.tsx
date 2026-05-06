import { useEffect, useState } from "react"
import { fetchRiskRules, upsertRiskRule } from "@/api/admin"
import type { AdminRiskRule } from "@/api/types"
import { Card } from "@/components/ui/Card"
import { Button } from "@/components/ui/Button"

export default function RiskRules() {
  const [rows, setRows] = useState<AdminRiskRule[]>([])
  const [error, setError] = useState<string | null>(null)
  const [loading, setLoading] = useState(false)

  const [code, setCode] = useState("")
  const [name, setName] = useState("")
  const [ruleType, setRuleType] = useState("trade")
  const [threshold, setThreshold] = useState<string>("")
  const [action, setAction] = useState("block")
  const [scoreDelta, setScoreDelta] = useState("-10")
  const [enabled, setEnabled] = useState(true)

  async function reload() {
    setLoading(true)
    setError(null)
    try {
      setRows(await fetchRiskRules())
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
        <div className="text-xl font-semibold">风控规则</div>
        <div className="mt-1 text-sm text-zinc-400">新增或更新规则（按 code upsert）</div>
      </div>

      <Card>
        <div className="grid gap-3 md:grid-cols-6">
          <div>
            <div className="text-sm text-zinc-300">code</div>
            <input className="mt-2 w-full rounded-xl border border-zinc-800 bg-zinc-950 px-3 py-2 text-sm outline-none focus:border-blue-600" value={code} onChange={(e) => setCode(e.target.value)} />
          </div>
          <div className="md:col-span-2">
            <div className="text-sm text-zinc-300">name</div>
            <input className="mt-2 w-full rounded-xl border border-zinc-800 bg-zinc-950 px-3 py-2 text-sm outline-none focus:border-blue-600" value={name} onChange={(e) => setName(e.target.value)} />
          </div>
          <div>
            <div className="text-sm text-zinc-300">rule_type</div>
            <input className="mt-2 w-full rounded-xl border border-zinc-800 bg-zinc-950 px-3 py-2 text-sm outline-none focus:border-blue-600" value={ruleType} onChange={(e) => setRuleType(e.target.value)} />
          </div>
          <div>
            <div className="text-sm text-zinc-300">threshold</div>
            <input className="mt-2 w-full rounded-xl border border-zinc-800 bg-zinc-950 px-3 py-2 text-sm outline-none focus:border-blue-600" value={threshold} onChange={(e) => setThreshold(e.target.value)} placeholder="可为空" />
          </div>
          <div>
            <div className="text-sm text-zinc-300">action</div>
            <input className="mt-2 w-full rounded-xl border border-zinc-800 bg-zinc-950 px-3 py-2 text-sm outline-none focus:border-blue-600" value={action} onChange={(e) => setAction(e.target.value)} />
          </div>
          <div>
            <div className="text-sm text-zinc-300">score_delta</div>
            <input className="mt-2 w-full rounded-xl border border-zinc-800 bg-zinc-950 px-3 py-2 text-sm outline-none focus:border-blue-600" value={scoreDelta} onChange={(e) => setScoreDelta(e.target.value)} />
          </div>
          <div className="flex items-end gap-3">
            <label className="flex items-center gap-2 text-sm text-zinc-300">
              <input type="checkbox" checked={enabled} onChange={(e) => setEnabled(e.target.checked)} />
              enabled
            </label>
          </div>
          <div className="flex items-end gap-3 md:col-span-2">
            <Button
              disabled={loading || !code.trim() || !name.trim()}
              onClick={async () => {
                setError(null)
                try {
                  const tv = threshold.trim() ? Number(threshold) : null
                  await upsertRiskRule({
                    code: code.trim(),
                    name: name.trim(),
                    rule_type: ruleType.trim(),
                    threshold_value: tv,
                    action: action.trim(),
                    score_delta: Number(scoreDelta),
                    enabled,
                  })
                  setCode("")
                  setName("")
                  setThreshold("")
                  await reload()
                } catch {
                  setError("保存失败")
                }
              }}
            >
              保存
            </Button>
            <Button variant="secondary" onClick={reload} disabled={loading}>
              {loading ? "刷新中..." : "刷新"}
            </Button>
          </div>
        </div>
        {error ? <div className="mt-4 rounded-xl border border-red-900 bg-red-950 px-3 py-2 text-sm text-red-200">{error}</div> : null}
      </Card>

      <div className="mt-4">
        <Card className="p-0">
          <div className="overflow-auto">
            <table className="min-w-[1100px] w-full text-left text-sm">
              <thead className="border-b border-zinc-800 text-zinc-400">
                <tr>
                  <th className="px-4 py-3">code</th>
                  <th className="px-4 py-3">name</th>
                  <th className="px-4 py-3">type</th>
                  <th className="px-4 py-3">threshold</th>
                  <th className="px-4 py-3">action</th>
                  <th className="px-4 py-3">score</th>
                  <th className="px-4 py-3">enabled</th>
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
                  rows.map((r) => (
                    <tr key={r.id} className="hover:bg-zinc-900/40">
                      <td className="px-4 py-3 font-mono text-xs">{r.code}</td>
                      <td className="px-4 py-3">{r.name}</td>
                      <td className="px-4 py-3">{r.rule_type}</td>
                      <td className="px-4 py-3">{r.threshold_value ?? "-"}</td>
                      <td className="px-4 py-3">{r.action}</td>
                      <td className="px-4 py-3">{r.score_delta}</td>
                      <td className="px-4 py-3">{r.enabled ? "yes" : "no"}</td>
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

