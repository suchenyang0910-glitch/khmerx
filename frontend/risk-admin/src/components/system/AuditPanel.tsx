import { useCallback, useEffect, useMemo, useState } from 'react'
import { getErrorMessage, requestJson } from '@/api/http'
import type { AuditLog, PageResponse } from '@/api/types'
import { useHasPermission } from '@/hooks/usePermission'

export default function AuditPanel() {
  const canRead = useHasPermission('audit.read')
  const [actorId, setActorId] = useState('')
  const [action, setAction] = useState('')
  const [objectType, setObjectType] = useState('')
  const [objectId, setObjectId] = useState('')
  const [page, setPage] = useState(1)
  const [pageSize] = useState(20)
  const [data, setData] = useState<PageResponse<AuditLog> | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const totalPages = useMemo(() => {
    const total = data?.total || 0
    return Math.max(1, Math.ceil(total / pageSize))
  }, [data?.total, pageSize])

  const load = useCallback(async () => {
    if (!canRead) return
    setLoading(true)
    setError(null)
    try {
      const qs = new URLSearchParams()
      if (actorId.trim()) qs.set('actorId', actorId.trim())
      if (action.trim()) qs.set('action', action.trim())
      if (objectType.trim()) qs.set('objectType', objectType.trim())
      if (objectId.trim()) qs.set('objectId', objectId.trim())
      qs.set('page', String(page))
      qs.set('pageSize', String(pageSize))
      const resp = await requestJson<PageResponse<AuditLog>>(`/api-risk/system/audit?${qs.toString()}`)
      setData(resp)
    } catch (e: unknown) {
      setError(getErrorMessage(e))
    } finally {
      setLoading(false)
    }
  }, [action, actorId, canRead, objectId, objectType, page, pageSize])

  useEffect(() => {
    load()
  }, [load])

  if (!canRead) {
    return <div className="rounded-2xl border border-zinc-200 bg-white p-6 text-sm text-zinc-600 shadow-sm">你没有 audit.read 权限</div>
  }

  return (
    <div className="space-y-3">
      <div className="rounded-2xl border border-zinc-200 bg-white p-4 shadow-sm">
        <div className="grid gap-3 md:grid-cols-4">
          <div>
            <label className="block text-xs text-zinc-500">actorId</label>
            <input
              value={actorId}
              onChange={(e) => setActorId(e.target.value)}
              className="mt-1 h-9 w-full rounded-lg border border-zinc-200 bg-white px-3 text-sm outline-none transition focus:border-zinc-400"
              placeholder="merchantId（可空）"
            />
          </div>
          <div>
            <label className="block text-xs text-zinc-500">action</label>
            <input
              value={action}
              onChange={(e) => setAction(e.target.value)}
              className="mt-1 h-9 w-full rounded-lg border border-zinc-200 bg-white px-3 text-sm outline-none transition focus:border-zinc-400"
              placeholder="例如 system.user.create"
            />
          </div>
          <div>
            <label className="block text-xs text-zinc-500">objectType</label>
            <input
              value={objectType}
              onChange={(e) => setObjectType(e.target.value)}
              className="mt-1 h-9 w-full rounded-lg border border-zinc-200 bg-white px-3 text-sm outline-none transition focus:border-zinc-400"
              placeholder="admin_user / role / risk_event"
            />
          </div>
          <div>
            <label className="block text-xs text-zinc-500">objectId</label>
            <input
              value={objectId}
              onChange={(e) => setObjectId(e.target.value)}
              className="mt-1 h-9 w-full rounded-lg border border-zinc-200 bg-white px-3 text-sm outline-none transition focus:border-zinc-400"
              placeholder="对象ID（可空）"
            />
          </div>
        </div>

        {error ? <div className="mt-3 rounded-lg border border-red-200 bg-red-50 px-3 py-2 text-sm text-red-700">{error}</div> : null}

        <div className="mt-3 flex items-center justify-between">
          <div className="text-xs text-zinc-500">共 {data?.total ?? 0} 条</div>
          <button
            type="button"
            onClick={() => {
              setPage(1)
              load()
            }}
            className="inline-flex h-9 items-center rounded-lg bg-zinc-900 px-3 text-sm font-medium text-white transition hover:bg-zinc-800"
          >
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
                <th className="px-3 py-2 text-left font-medium">actor</th>
                <th className="px-3 py-2 text-left font-medium">action</th>
                <th className="px-3 py-2 text-left font-medium">object</th>
                <th className="px-3 py-2 text-left font-medium">ip</th>
              </tr>
            </thead>
            <tbody>
              {(data?.items || []).map((l) => (
                <tr key={l.logId} className="border-t border-zinc-200">
                  <td className="px-3 py-2 text-xs text-zinc-600">{l.createdAt || '—'}</td>
                  <td className="px-3 py-2 font-mono text-xs text-zinc-700">{l.actorId || '—'}</td>
                  <td className="px-3 py-2 text-zinc-700">{l.action}</td>
                  <td className="px-3 py-2">
                    <div className="text-zinc-900">{l.objectType}</div>
                    <div className="font-mono text-xs text-zinc-500">{l.objectId || '—'}</div>
                  </td>
                  <td className="px-3 py-2 text-xs text-zinc-600">{l.ip || '—'}</td>
                </tr>
              ))}
              {!loading && (data?.items || []).length === 0 ? (
                <tr>
                  <td className="px-3 py-10 text-center text-sm text-zinc-500" colSpan={5}>
                    暂无数据
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
    </div>
  )
}

