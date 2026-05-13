import { useCallback, useEffect, useMemo, useState } from 'react'
import { Search } from 'lucide-react'
import { getErrorMessage, requestJson } from '@/api/http'
import type { PageResponse, RiskEvent, RiskEventDetailResponse } from '@/api/types'
import { cn } from '@/lib/utils'
import EventDetailDrawer from '@/components/cases/EventDetailDrawer'
import { useHasPermission } from '@/hooks/usePermission'

export default function Cases() {
  const canDispose = useHasPermission('cases.dispose')
  const [scenarioType, setScenarioType] = useState('')
  const [keyword, setKeyword] = useState('')
  const [status, setStatus] = useState('')
  const [page, setPage] = useState(1)
  const [pageSize] = useState(20)
  const [data, setData] = useState<PageResponse<RiskEvent> | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const [selectedEventId, setSelectedEventId] = useState<string | null>(null)
  const [detail, setDetail] = useState<RiskEventDetailResponse | null>(null)
  const [detailLoading, setDetailLoading] = useState(false)
  const [detailError, setDetailError] = useState<string | null>(null)

  const totalPages = useMemo(() => {
    const total = data?.total || 0
    return Math.max(1, Math.ceil(total / pageSize))
  }, [data?.total, pageSize])

  const load = useCallback(async () => {
    setLoading(true)
    setError(null)
    try {
      const qs = new URLSearchParams()
      if (scenarioType.trim()) qs.set('scenarioType', scenarioType.trim())
      if (keyword.trim()) qs.set('keyword', keyword.trim())
      if (status.trim()) qs.set('status', status.trim())
      qs.set('page', String(page))
      qs.set('pageSize', String(pageSize))
      const resp = await requestJson<PageResponse<RiskEvent>>(`/api-risk/risk/events?${qs.toString()}`)
      setData(resp)
    } catch (e: unknown) {
      setError(getErrorMessage(e))
    } finally {
      setLoading(false)
    }
  }, [keyword, page, pageSize, scenarioType, status])

  const loadDetail = useCallback(async (eventId: string) => {
    setDetailLoading(true)
    setDetailError(null)
    try {
      const resp = await requestJson<RiskEventDetailResponse>(`/api-risk/risk/events/${encodeURIComponent(eventId)}`)
      setDetail(resp)
    } catch (e: unknown) {
      setDetailError(getErrorMessage(e))
    } finally {
      setDetailLoading(false)
    }
  }, [])

  useEffect(() => {
    load()
  }, [load])

  useEffect(() => {
    if (!selectedEventId) {
      setDetail(null)
      setDetailError(null)
      return
    }
    loadDetail(selectedEventId)
  }, [loadDetail, selectedEventId])

  const submitDisposition = useCallback(
    async (action: string, remark: string) => {
      if (!selectedEventId) return
      setDetailError(null)
      try {
        await requestJson(`/api-risk/risk/events/${encodeURIComponent(selectedEventId)}/dispositions`, {
          method: 'POST',
          body: JSON.stringify({ action, remark }),
        })
        await loadDetail(selectedEventId)
        await load()
      } catch (e: unknown) {
        setDetailError(getErrorMessage(e))
      }
    },
    [load, loadDetail, selectedEventId]
  )

  return (
    <div className="space-y-4">
      <div>
        <div className="text-base font-semibold">命中处置</div>
        <div className="text-xs text-zinc-500">检索命中事件、查看详情并执行处置（数据来自 risk-engine-service）</div>
      </div>

      <div className="rounded-2xl border border-zinc-200 bg-white p-4 shadow-sm">
        <div className="grid gap-3 md:grid-cols-3">
          <div>
            <label className="block text-xs text-zinc-500">场景</label>
            <input
              value={scenarioType}
              onChange={(e) => setScenarioType(e.target.value)}
              className="mt-1 h-9 w-full rounded-lg border border-zinc-200 bg-white px-3 text-sm outline-none transition focus:border-zinc-400"
              placeholder="例如 phone_rental（可空）"
            />
          </div>
          <div>
            <label className="block text-xs text-zinc-500">关键字</label>
            <input
              value={keyword}
              onChange={(e) => setKeyword(e.target.value)}
              className="mt-1 h-9 w-full rounded-lg border border-zinc-200 bg-white px-3 text-sm outline-none transition focus:border-zinc-400"
              placeholder="eventId / userId / orderId / ruleId"
            />
          </div>
          <div>
            <label className="block text-xs text-zinc-500">状态</label>
            <input
              value={status}
              onChange={(e) => setStatus(e.target.value)}
              className="mt-1 h-9 w-full rounded-lg border border-zinc-200 bg-white px-3 text-sm outline-none transition focus:border-zinc-400"
              placeholder="open / processing / closed（可空）"
            />
          </div>
        </div>

        {error ? <div className="mt-3 rounded-lg border border-red-200 bg-red-50 px-3 py-2 text-sm text-red-700">{error}</div> : null}

        <div className="mt-3 flex items-center justify-between gap-2">
          <div className="text-xs text-zinc-500">共 {data?.total ?? 0} 条</div>
          <button
            type="button"
            onClick={() => {
              setPage(1)
              load()
            }}
            className="inline-flex h-9 items-center gap-2 rounded-lg bg-zinc-900 px-3 text-sm font-medium text-white transition hover:bg-zinc-800"
          >
            <Search className="h-4 w-4" />
            查询
          </button>
        </div>
      </div>

      <div className="rounded-2xl border border-zinc-200 bg-white p-4 shadow-sm">
        <div className="overflow-hidden rounded-xl border border-zinc-200">
          <table className="w-full text-sm">
            <thead className="bg-zinc-50 text-xs text-zinc-500">
              <tr>
                <th className="px-3 py-2 text-left font-medium">时间</th>
                <th className="px-3 py-2 text-left font-medium">场景</th>
                <th className="px-3 py-2 text-left font-medium">userId / orderId</th>
                <th className="px-3 py-2 text-left font-medium">决策</th>
                <th className="px-3 py-2 text-left font-medium">等级</th>
                <th className="px-3 py-2 text-left font-medium">状态</th>
              </tr>
            </thead>
            <tbody>
              {(data?.items || []).map((e) => (
                <tr
                  key={e.eventId}
                  className="cursor-pointer border-t border-zinc-200 hover:bg-zinc-50"
                  onClick={() => setSelectedEventId(e.eventId)}
                >
                  <td className="px-3 py-2 text-xs text-zinc-600">{e.createdAt || '—'}</td>
                  <td className="px-3 py-2 text-zinc-700">{e.scenarioType || '—'}</td>
                  <td className="px-3 py-2">
                    <div className="text-zinc-900">{e.userId || '—'}</div>
                    <div className="text-xs text-zinc-500">{e.orderId || '—'}</div>
                  </td>
                  <td className="px-3 py-2 text-zinc-700">{e.decision || '—'}</td>
                  <td className="px-3 py-2 text-zinc-700">{e.riskLevel || '—'}</td>
                  <td className="px-3 py-2">
                    <span
                      className={cn(
                        'inline-flex rounded-full px-2 py-0.5 text-xs',
                        e.status === 'open'
                          ? 'bg-sky-50 text-sky-700'
                          : e.status === 'processing'
                            ? 'bg-amber-50 text-amber-700'
                            : 'bg-emerald-50 text-emerald-700'
                      )}
                    >
                      {e.status}
                    </span>
                  </td>
                </tr>
              ))}
              {!loading && (data?.items || []).length === 0 ? (
                <tr>
                  <td className="px-3 py-10 text-center text-sm text-zinc-500" colSpan={6}>
                    暂无数据（需要先调用 /risk/check 产生事件）
                  </td>
                </tr>
              ) : null}
            </tbody>
          </table>
        </div>

        <div className="mt-3 flex items-center justify-between">
          <div className="text-xs text-zinc-500">第 {page} / {totalPages} 页</div>
          <div className="flex items-center gap-2">
            <button
              type="button"
              onClick={() => setPage((p) => Math.max(1, p - 1))}
              disabled={page <= 1}
              className="inline-flex h-9 items-center rounded-lg border border-zinc-200 bg-white px-3 text-sm text-zinc-700 transition hover:bg-zinc-50 disabled:cursor-not-allowed disabled:opacity-50"
            >
              上一页
            </button>
            <button
              type="button"
              onClick={() => setPage((p) => Math.min(totalPages, p + 1))}
              disabled={page >= totalPages}
              className="inline-flex h-9 items-center rounded-lg border border-zinc-200 bg-white px-3 text-sm text-zinc-700 transition hover:bg-zinc-50 disabled:cursor-not-allowed disabled:opacity-50"
            >
              下一页
            </button>
          </div>
        </div>
      </div>

      <EventDetailDrawer
        open={!!selectedEventId}
        eventId={selectedEventId}
        detail={detail}
        loading={detailLoading}
        error={detailError}
        canDispose={canDispose}
        onClose={() => {
          setSelectedEventId(null)
          setDetail(null)
        }}
        onSubmitDisposition={submitDisposition}
      />
    </div>
  )
}
