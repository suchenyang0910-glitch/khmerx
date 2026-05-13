import { useCallback, useEffect, useMemo, useState } from 'react'
import type { RiskRule } from '@/api/types'
import { getErrorMessage, requestJson } from '@/api/http'
import { RefreshCcw, Search } from 'lucide-react'
import { cn } from '@/lib/utils'
import { useHasPermission } from '@/hooks/usePermission'

export default function Rules() {
  const canPublish = useHasPermission('rules.publish')
  const [scenarioType, setScenarioType] = useState('phone_rental')
  const [rules, setRules] = useState<RiskRule[]>([])
  const [query, setQuery] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [reloading, setReloading] = useState(false)

  const filtered = useMemo(() => {
    const q = query.trim().toLowerCase()
    if (!q) return rules
    return rules.filter((r) => {
      return (
        r.ruleId.toLowerCase().includes(q) ||
        r.ruleName.toLowerCase().includes(q) ||
        r.ruleExpression.toLowerCase().includes(q) ||
        r.riskAction.toLowerCase().includes(q)
      )
    })
  }, [rules, query])

  const load = useCallback(async () => {
    setLoading(true)
    setError(null)
    try {
      const data = await requestJson<RiskRule[]>(`/api-risk/risk/rules?scenarioType=${encodeURIComponent(scenarioType)}`)
      setRules(data)
    } catch (e: unknown) {
      setError(getErrorMessage(e))
    } finally {
      setLoading(false)
    }
  }, [scenarioType])

  async function reload() {
    setReloading(true)
    setError(null)
    try {
      await requestJson(`/api-risk/risk/rules/reload?scenarioType=${encodeURIComponent(scenarioType)}`, { method: 'POST' })
      await load()
    } catch (e: unknown) {
      setError(getErrorMessage(e))
    } finally {
      setReloading(false)
    }
  }

  useEffect(() => {
    load()
  }, [load])

  return (
    <div className="space-y-4">
      <div className="flex flex-wrap items-end justify-between gap-3">
        <div>
          <div className="text-base font-semibold">规则管理</div>
          <div className="text-xs text-zinc-500">当前版本对接 risk-engine-service 的规则读取与缓存刷新接口</div>
        </div>

        <div className="flex flex-wrap items-center gap-2">
          <div className="flex items-center gap-2">
            <label className="text-xs text-zinc-500">场景</label>
            <input
              value={scenarioType}
              onChange={(e) => setScenarioType(e.target.value)}
              className="h-9 w-56 rounded-lg border border-zinc-200 bg-white px-3 text-sm outline-none transition focus:border-zinc-400"
            />
          </div>

          <button
            type="button"
            onClick={reload}
            disabled={reloading || !canPublish}
            className="inline-flex h-9 items-center gap-2 rounded-lg border border-zinc-200 bg-white px-3 text-sm text-zinc-700 transition hover:bg-zinc-50 disabled:cursor-not-allowed disabled:opacity-50"
          >
            <RefreshCcw className={cn('h-4 w-4', reloading ? 'animate-spin' : '')} />
            刷新缓存
          </button>
        </div>
      </div>

      <div className="rounded-2xl border border-zinc-200 bg-white p-4 shadow-sm">
        <div className="flex flex-wrap items-center justify-between gap-2">
          <div className="text-sm font-medium">规则列表</div>
          <div className="relative">
            <Search className="pointer-events-none absolute left-3 top-2.5 h-4 w-4 text-zinc-400" />
            <input
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              className="h-9 w-72 rounded-lg border border-zinc-200 bg-white pl-9 pr-3 text-sm outline-none transition focus:border-zinc-400"
              placeholder="搜索 ruleId / 名称 / 表达式 / 动作"
            />
          </div>
        </div>

        {error ? <div className="mt-3 rounded-lg border border-red-200 bg-red-50 px-3 py-2 text-sm text-red-700">{error}</div> : null}

        <div className="mt-3 overflow-hidden rounded-xl border border-zinc-200">
          <table className="w-full text-sm">
            <thead className="bg-zinc-50 text-xs text-zinc-500">
              <tr>
                <th className="px-3 py-2 text-left font-medium">规则</th>
                <th className="px-3 py-2 text-left font-medium">表达式</th>
                <th className="px-3 py-2 text-left font-medium">动作</th>
                <th className="px-3 py-2 text-left font-medium">扣分</th>
                <th className="px-3 py-2 text-left font-medium">状态</th>
              </tr>
            </thead>
            <tbody>
              {filtered.map((r) => (
                <tr key={r.ruleId} className="border-t border-zinc-200">
                  <td className="px-3 py-2">
                    <div className="font-medium text-zinc-900">{r.ruleName}</div>
                    <div className="truncate text-xs text-zinc-500">{r.ruleId}</div>
                  </td>
                  <td className="px-3 py-2">
                    <div className="max-w-xl truncate font-mono text-xs text-zinc-700">{r.ruleExpression}</div>
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
              {!loading && filtered.length === 0 ? (
                <tr>
                  <td className="px-3 py-6 text-center text-sm text-zinc-500" colSpan={5}>
                    暂无数据
                  </td>
                </tr>
              ) : null}
            </tbody>
          </table>
        </div>

        <div className="mt-3 text-xs text-zinc-500">
          新增/编辑/发布接口后，将在此页面启用“草稿/版本/发布/回滚”完整流程。
        </div>
      </div>
    </div>
  )
}
