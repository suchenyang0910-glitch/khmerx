import { useEffect, useMemo, useState } from 'react'
import { getErrorMessage, requestJson } from '@/api/http'
import type { RiskRule } from '@/api/types'
import { SlidersHorizontal, ShieldAlert, ClipboardList } from 'lucide-react'
import { cn } from '@/lib/utils'
import { useHasPermission } from '@/hooks/usePermission'

function StatCard(props: { title: string; value: string; icon: React.ReactNode; tone?: 'neutral' | 'warn' }) {
  return (
    <div
      className={cn(
        'rounded-2xl border border-zinc-200 bg-white p-4 shadow-sm',
        props.tone === 'warn' ? 'border-amber-200 bg-amber-50' : ''
      )}
    >
      <div className="flex items-center justify-between">
        <div>
          <div className="text-xs text-zinc-500">{props.title}</div>
          <div className="mt-1 text-lg font-semibold text-zinc-900">{props.value}</div>
        </div>
        <div className="text-zinc-700">{props.icon}</div>
      </div>
    </div>
  )
}

export default function Dashboard() {
  const canReadRules = useHasPermission('rules.read')
  const [scenarioType, setScenarioType] = useState('phone_rental')
  const [rules, setRules] = useState<RiskRule[]>([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const enabledCount = useMemo(() => rules.filter((r) => r.status === 1).length, [rules])

  useEffect(() => {
    let mounted = true
    async function load() {
      if (!canReadRules) {
        if (mounted) {
          setRules([])
          setError(null)
          setLoading(false)
        }
        return
      }
      setLoading(true)
      setError(null)
      try {
        const data = await requestJson<RiskRule[]>(`/api-risk/risk/rules?scenarioType=${encodeURIComponent(scenarioType)}`)
        if (mounted) setRules(data)
      } catch (e: unknown) {
        if (mounted) setError(getErrorMessage(e))
      } finally {
        if (mounted) setLoading(false)
      }
    }
    load()
    return () => {
      mounted = false
    }
  }, [canReadRules, scenarioType])

  return (
    <div className="space-y-4">
      <div className="flex flex-wrap items-end justify-between gap-3">
        <div>
          <div className="text-base font-semibold">控制台</div>
          <div className="text-xs text-zinc-500">当前版本展示规则与基础运行状态</div>
        </div>
        <div className="flex items-center gap-2">
          <label className="text-xs text-zinc-500">场景</label>
          <input
            value={scenarioType}
            onChange={(e) => setScenarioType(e.target.value)}
            className="h-9 w-56 rounded-lg border border-zinc-200 bg-white px-3 text-sm outline-none transition focus:border-zinc-400"
          />
        </div>
      </div>

      <div className="grid gap-3 md:grid-cols-2 xl:grid-cols-4">
        <StatCard title="启用规则数" value={loading ? '加载中…' : String(enabledCount)} icon={<SlidersHorizontal className="h-5 w-5" />} />
        <StatCard title="命中量（今日）" value="—" icon={<ShieldAlert className="h-5 w-5" />} />
        <StatCard title="处置完成率（今日）" value="—" icon={<ClipboardList className="h-5 w-5" />} />
        <StatCard title="告警" value={error ? '异常' : '—'} icon={<ShieldAlert className="h-5 w-5" />} tone={error ? 'warn' : 'neutral'} />
      </div>

      <div className="rounded-2xl border border-zinc-200 bg-white p-4 shadow-sm">
        <div className="flex items-center justify-between">
          <div>
            <div className="text-sm font-medium">最近规则（按加载结果展示）</div>
            <div className="text-xs text-zinc-500">后续接入发布记录与命中事件后将展示真实指标</div>
          </div>
        </div>

        {!canReadRules ? (
          <div className="mt-3 rounded-lg border border-zinc-200 bg-zinc-50 px-3 py-2 text-sm text-zinc-600">你没有 rules.read 权限</div>
        ) : null}

        {error ? <div className="mt-3 rounded-lg border border-red-200 bg-red-50 px-3 py-2 text-sm text-red-700">{error}</div> : null}

        <div className="mt-3 overflow-hidden rounded-xl border border-zinc-200">
          <table className="w-full text-sm">
            <thead className="bg-zinc-50 text-xs text-zinc-500">
              <tr>
                <th className="px-3 py-2 text-left font-medium">规则</th>
                <th className="px-3 py-2 text-left font-medium">动作</th>
                <th className="px-3 py-2 text-left font-medium">扣分</th>
                <th className="px-3 py-2 text-left font-medium">状态</th>
              </tr>
            </thead>
            <tbody>
              {rules.slice(0, 6).map((r) => (
                <tr key={r.ruleId} className="border-t border-zinc-200">
                  <td className="px-3 py-2">
                    <div className="font-medium text-zinc-900">{r.ruleName}</div>
                    <div className="truncate text-xs text-zinc-500">{r.ruleId}</div>
                  </td>
                  <td className="px-3 py-2 text-zinc-700">{r.riskAction}</td>
                  <td className="px-3 py-2 text-zinc-700">{r.scoreWeight}</td>
                  <td className="px-3 py-2">
                    <span
                      className={cn(
                        'inline-flex rounded-full px-2 py-0.5 text-xs',
                        r.status === 1 ? 'bg-emerald-50 text-emerald-700' : 'bg-zinc-100 text-zinc-600'
                      )}
                    >
                      {r.status === 1 ? '启用' : '停用'}
                    </span>
                  </td>
                </tr>
              ))}
              {!loading && rules.length === 0 ? (
                <tr>
                  <td className="px-3 py-6 text-center text-sm text-zinc-500" colSpan={4}>
                    暂无规则
                  </td>
                </tr>
              ) : null}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  )
}
