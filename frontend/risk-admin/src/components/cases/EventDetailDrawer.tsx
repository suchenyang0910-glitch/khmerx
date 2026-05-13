import { useMemo, useState } from 'react'
import { Save, ShieldAlert } from 'lucide-react'
import Drawer from '@/components/Drawer'
import type { Disposition, RiskEventDetailResponse } from '@/api/types'

export default function EventDetailDrawer(props: {
  open: boolean
  eventId: string | null
  detail: RiskEventDetailResponse | null
  loading: boolean
  error: string | null
  canDispose: boolean
  onClose: () => void
  onSubmitDisposition: (action: string, remark: string) => Promise<void>
}) {
  type Action = 'allow' | 'block' | 'manual_review' | 'whitelist' | 'blacklist'
  const [action, setAction] = useState<Action>('manual_review')
  const [remark, setRemark] = useState('')
  const [submitting, setSubmitting] = useState(false)

  const dispositions = useMemo<Disposition[]>(() => props.detail?.dispositions || [], [props.detail])

  async function submit() {
    if (!props.eventId) return
    setSubmitting(true)
    try {
      await props.onSubmitDisposition(action, remark)
      setRemark('')
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <Drawer
      open={props.open}
      title={props.eventId ? `事件详情：${props.eventId}` : '事件详情'}
      onClose={props.onClose}
    >
      {props.error ? <div className="rounded-lg border border-red-200 bg-red-50 px-3 py-2 text-sm text-red-700">{props.error}</div> : null}
      {props.loading ? <div className="text-sm text-zinc-600">加载中…</div> : null}

      {props.detail?.event ? (
        <div className="space-y-4">
          <div className="rounded-2xl border border-zinc-200 bg-zinc-50 p-4">
            <div className="flex items-start justify-between gap-3">
              <div>
                <div className="text-sm font-semibold text-zinc-900">{props.detail.event.scenarioType || '—'}</div>
                <div className="mt-1 text-xs text-zinc-500">merchant: {props.detail.event.merchantId}</div>
              </div>
              <span className="inline-flex items-center gap-1 rounded-full bg-white px-3 py-1 text-xs text-zinc-700 ring-1 ring-zinc-200">
                <ShieldAlert className="h-3.5 w-3.5" />
                {props.detail.event.decision}
              </span>
            </div>
            <div className="mt-3 grid gap-2">
              <div className="flex items-center justify-between gap-3">
                <div className="text-xs text-zinc-500">userId</div>
                <div className="font-mono text-xs text-zinc-900">{props.detail.event.userId || '—'}</div>
              </div>
              <div className="flex items-center justify-between gap-3">
                <div className="text-xs text-zinc-500">orderId</div>
                <div className="font-mono text-xs text-zinc-900">{props.detail.event.orderId || '—'}</div>
              </div>
              <div className="flex items-center justify-between gap-3">
                <div className="text-xs text-zinc-500">risk</div>
                <div className="text-xs text-zinc-900">{props.detail.event.riskLevel} / {props.detail.event.riskScore}</div>
              </div>
              <div className="flex items-center justify-between gap-3">
                <div className="text-xs text-zinc-500">reason</div>
                <div className="text-xs text-zinc-900">{props.detail.event.reason || '—'}</div>
              </div>
              <div className="flex items-center justify-between gap-3">
                <div className="text-xs text-zinc-500">matchedRuleIds</div>
                <div className="text-xs text-zinc-900">{props.detail.event.matchedRuleIds || '—'}</div>
              </div>
            </div>
          </div>

          <div className="rounded-2xl border border-zinc-200 bg-white p-4">
            <div className="text-sm font-medium">处置</div>
            <div className="mt-3 grid gap-3">
              <div className="grid gap-3 md:grid-cols-2">
                <div>
                  <label className="block text-xs text-zinc-500">动作</label>
                  <select
                    value={action}
                    onChange={(e) => setAction(e.target.value as Action)}
                    className="mt-1 h-9 w-full rounded-lg border border-zinc-200 bg-white px-3 text-sm outline-none transition focus:border-zinc-400"
                  >
                    <option value="manual_review">manual_review</option>
                    <option value="allow">allow</option>
                    <option value="block">block</option>
                    <option value="whitelist">whitelist</option>
                    <option value="blacklist">blacklist</option>
                  </select>
                </div>
                <div>
                  <label className="block text-xs text-zinc-500">备注</label>
                  <input
                    value={remark}
                    onChange={(e) => setRemark(e.target.value)}
                    className="mt-1 h-9 w-full rounded-lg border border-zinc-200 bg-white px-3 text-sm outline-none transition focus:border-zinc-400"
                    placeholder="处置原因/说明"
                  />
                </div>
              </div>
              <button
                type="button"
                onClick={submit}
                disabled={submitting || !props.canDispose}
                className="inline-flex h-9 items-center justify-center gap-2 rounded-lg bg-zinc-900 px-3 text-sm font-medium text-white transition hover:bg-zinc-800 disabled:cursor-not-allowed disabled:opacity-50"
              >
                <Save className="h-4 w-4" />
                {submitting ? '提交中…' : '提交处置'}
              </button>
              {!props.canDispose ? <div className="text-xs text-zinc-500">你没有 cases.dispose 权限，处置按钮已禁用</div> : null}
            </div>

            <div className="mt-4">
              <div className="text-sm font-medium">处置历史</div>
              <div className="mt-2 space-y-2">
                {dispositions.map((d) => (
                  <div key={d.dispositionId} className="rounded-xl border border-zinc-200 bg-white p-3">
                    <div className="flex items-center justify-between">
                      <div className="text-sm font-medium text-zinc-900">{d.action}</div>
                      <div className="text-xs text-zinc-500">{d.createdAt || '—'}</div>
                    </div>
                    <div className="mt-1 text-xs text-zinc-600">operator: {d.operatorId || '—'}</div>
                    {d.remark ? <div className="mt-2 text-sm text-zinc-700">{d.remark}</div> : null}
                  </div>
                ))}
                {dispositions.length === 0 ? <div className="text-sm text-zinc-500">暂无处置记录</div> : null}
              </div>
            </div>
          </div>

          <div className="rounded-2xl border border-zinc-200 bg-white p-4">
            <div className="text-sm font-medium">输入快照</div>
            <pre className="mt-2 max-h-80 overflow-auto rounded-xl border border-zinc-200 bg-zinc-50 p-3 text-xs text-zinc-800">
              {props.detail.event.inputSnapshot || '—'}
            </pre>
          </div>
        </div>
      ) : null}
    </Drawer>
  )
}
