import { useEffect, useMemo, useState } from "react"
import { fetchInterestRates, upsertInterestRate } from "@/api/admin"
import type { AdminInterestRate } from "@/api/types"
import { Button } from "@/components/ui/Button"
import { Card } from "@/components/ui/Card"

export default function InterestRates() {
  const [rows, setRows] = useState<AdminInterestRate[]>([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const [termDays, setTermDays] = useState(7)
  const [creditLevel, setCreditLevel] = useState("A")
  const [ratePercent, setRatePercent] = useState("10")

  const valid = useMemo(() => {
    const rate = Number(ratePercent)
    return [7, 14, 30].includes(termDays) && ["A", "B", "C", "D"].includes(creditLevel) && Number.isFinite(rate) && rate >= 0
  }, [termDays, creditLevel, ratePercent])

  async function reload() {
    setLoading(true)
    setError(null)
    try {
      setRows(await fetchInterestRates())
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
        <div className="text-xl font-semibold">利率矩阵</div>
        <div className="mt-1 text-sm text-zinc-400">设置 term_days + credit_level 的 rate_percent</div>
      </div>

      <Card>
        <div className="grid gap-3 md:grid-cols-4">
          <div>
            <div className="text-sm text-zinc-300">期限</div>
            <select
              className="mt-2 w-full rounded-xl border border-zinc-800 bg-zinc-950 px-3 py-2 text-sm outline-none focus:border-blue-600"
              value={termDays}
              onChange={(e) => setTermDays(Number(e.target.value))}
            >
              <option value={7}>7 天</option>
              <option value={14}>14 天</option>
              <option value={30}>30 天</option>
            </select>
          </div>
          <div>
            <div className="text-sm text-zinc-300">信用等级</div>
            <select
              className="mt-2 w-full rounded-xl border border-zinc-800 bg-zinc-950 px-3 py-2 text-sm outline-none focus:border-blue-600"
              value={creditLevel}
              onChange={(e) => setCreditLevel(e.target.value)}
            >
              <option value="A">A</option>
              <option value="B">B</option>
              <option value="C">C</option>
              <option value="D">D</option>
            </select>
          </div>
          <div>
            <div className="text-sm text-zinc-300">利率(%)</div>
            <input
              className="mt-2 w-full rounded-xl border border-zinc-800 bg-zinc-950 px-3 py-2 text-sm outline-none focus:border-blue-600"
              value={ratePercent}
              onChange={(e) => setRatePercent(e.target.value)}
            />
          </div>
          <div className="flex items-end gap-3">
            <Button
              disabled={!valid || loading}
              onClick={async () => {
                setError(null)
                try {
                  await upsertInterestRate({ term_days: termDays, credit_level: creditLevel, rate_percent: Number(ratePercent) })
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
            <table className="min-w-[760px] w-full text-left text-sm">
              <thead className="border-b border-zinc-800 text-zinc-400">
                <tr>
                  <th className="px-4 py-3">term_days</th>
                  <th className="px-4 py-3">credit_level</th>
                  <th className="px-4 py-3">rate_percent</th>
                  <th className="px-4 py-3">mode</th>
                  <th className="px-4 py-3">enabled</th>
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
                  rows.map((r) => (
                    <tr key={r.id} className="hover:bg-zinc-900/40">
                      <td className="px-4 py-3">{r.term_days}</td>
                      <td className="px-4 py-3">{r.credit_level}</td>
                      <td className="px-4 py-3">{r.rate_percent}</td>
                      <td className="px-4 py-3">{r.mode}</td>
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

