import Drawer from '@/components/Drawer'
import type { CollectionDetail, CollectionRow } from '@/components/salaryLoan/types'

export default function CollectionDrawer(props: {
  open: boolean
  selected: CollectionRow | null
  detail: CollectionDetail | null
  loading: boolean
  error: string | null
  actionLoading: boolean
  followResult: string
  setFollowResult: (v: string) => void
  followReasonCode: string
  setFollowReasonCode: (v: string) => void
  followNote: string
  setFollowNote: (v: string) => void
  followChannel: string
  setFollowChannel: (v: string) => void
  followPtpDate: string
  setFollowPtpDate: (v: string) => void
  followPtpAmount: string
  setFollowPtpAmount: (v: string) => void
  nextFollowUpAt: string
  setNextFollowUpAt: (v: string) => void
  onClose: () => void
  onCreateEvent: () => void
}) {
  return (
    <Drawer
      open={props.open}
      title={props.selected ? `催收案件 ${props.selected.order_id.slice(0, 8)}` : '催收案件'}
      onClose={props.onClose}
      widthClassName="max-w-3xl"
    >
      {props.error ? (
        <div className="mb-3 rounded-lg border border-red-200 bg-red-50 px-3 py-2 text-sm text-red-700">{props.error}</div>
      ) : null}

      {props.loading ? (
        <div className="text-sm text-zinc-600">加载中…</div>
      ) : !props.detail ? (
        <div className="text-sm text-zinc-600">暂无数据</div>
      ) : (
        <div className="space-y-4">
          <div className="grid grid-cols-1 gap-3 md:grid-cols-3">
            <div className="rounded-2xl border border-zinc-200 bg-white p-4">
              <div className="text-xs text-zinc-500">DPD / 阶段</div>
              <div className="mt-1 text-lg font-semibold text-zinc-900">
                {props.detail.case.dpd} / {props.detail.case.stage}
              </div>
            </div>
            <div className="rounded-2xl border border-zinc-200 bg-white p-4">
              <div className="text-xs text-zinc-500">案件状态</div>
              <div className="mt-1 text-lg font-semibold text-zinc-900">{props.detail.case.status}</div>
            </div>
            <div className="rounded-2xl border border-zinc-200 bg-white p-4">
              <div className="text-xs text-zinc-500">跟进人</div>
              <div className="mt-1 text-lg font-semibold text-zinc-900">{props.detail.case.assignee || '-'}</div>
            </div>
          </div>

          <div className="grid grid-cols-1 gap-4 md:grid-cols-2">
            <div className="rounded-2xl border border-zinc-200 bg-white p-4">
              <div className="text-sm font-semibold text-zinc-900">订单信息</div>
              {props.detail.order ? (
                <div className="mt-3 space-y-2 text-sm text-zinc-700">
                  <div>状态：{props.detail.order.status}</div>
                  <div>本金：${props.detail.order.principal.toFixed(2)}</div>
                  <div>应还：${props.detail.order.total_due.toFixed(2)}</div>
                  <div>到账：${props.detail.order.disbursement_amount.toFixed(2)}</div>
                  <div>到期：{props.detail.order.due_date || '-'}</div>
                  <div>风险分：{props.detail.order.risk_score ?? '-'}</div>
                </div>
              ) : (
                <div className="mt-3 text-sm text-zinc-500">暂无订单信息</div>
              )}
            </div>

            <div className="rounded-2xl border border-zinc-200 bg-white p-4">
              <div className="text-sm font-semibold text-zinc-900">企业与就业</div>
              <div className="mt-3 space-y-2 text-sm text-zinc-700">
                <div>企业：{props.detail.factory?.name || '-'}</div>
                <div>地点：{props.detail.factory?.location || '-'}</div>
                <div>企业风险：{props.detail.factory?.risk_level || '-'}</div>
                <div>HR：{props.detail.factory?.hr_contact || '-'}</div>
                <div>工号：{props.detail.employment?.employee_no || '-'}</div>
                <div>就业验证：{props.detail.employment?.verify_status || '-'}</div>
              </div>
            </div>
          </div>

          <div className="rounded-2xl border border-zinc-200 bg-white p-4">
            <div className="text-sm font-semibold text-zinc-900">新增跟进记录</div>
            <div className="mt-3 grid grid-cols-1 gap-3 md:grid-cols-2">
              <select
                value={props.followChannel}
                onChange={(e) => props.setFollowChannel(e.target.value)}
                className="h-9 rounded-lg border border-zinc-200 bg-white px-3 text-sm"
              >
                <option value="call">call</option>
                <option value="whatsapp">whatsapp</option>
                <option value="sms">sms</option>
                <option value="field">field</option>
              </select>
              <input
                value={props.followResult}
                onChange={(e) => props.setFollowResult(e.target.value)}
                placeholder="跟进结果，如 connected / ptp / no_answer"
                className="h-9 rounded-lg border border-zinc-200 px-3 text-sm"
              />
              <input
                value={props.followReasonCode}
                onChange={(e) => props.setFollowReasonCode(e.target.value)}
                placeholder="原因码，如 promise_to_pay"
                className="h-9 rounded-lg border border-zinc-200 px-3 text-sm"
              />
              <input
                type="datetime-local"
                value={props.nextFollowUpAt}
                onChange={(e) => props.setNextFollowUpAt(e.target.value)}
                className="h-9 rounded-lg border border-zinc-200 px-3 text-sm"
              />
              <input
                type="date"
                value={props.followPtpDate}
                onChange={(e) => props.setFollowPtpDate(e.target.value)}
                className="h-9 rounded-lg border border-zinc-200 px-3 text-sm"
              />
              <input
                value={props.followPtpAmount}
                onChange={(e) => props.setFollowPtpAmount(e.target.value)}
                placeholder="PTP 金额"
                className="h-9 rounded-lg border border-zinc-200 px-3 text-sm"
              />
              <textarea
                value={props.followNote}
                onChange={(e) => props.setFollowNote(e.target.value)}
                placeholder="跟进备注"
                className="min-h-24 rounded-lg border border-zinc-200 px-3 py-2 text-sm md:col-span-2"
              />
            </div>
            <div className="mt-3">
              <button
                type="button"
                disabled={props.actionLoading || !props.followResult.trim()}
                onClick={props.onCreateEvent}
                className="inline-flex h-9 items-center justify-center rounded-lg bg-zinc-900 px-4 text-sm font-medium text-white disabled:opacity-50"
              >
                保存跟进
              </button>
            </div>
          </div>

          <div className="rounded-2xl border border-zinc-200 bg-white p-4">
            <div className="text-sm font-semibold text-zinc-900">跟进时间线</div>
            <div className="mt-3 space-y-3">
              {props.detail.events.length === 0 ? (
                <div className="text-sm text-zinc-500">暂无跟进记录</div>
              ) : (
                props.detail.events.map((event) => (
                  <div key={event.id} className="rounded-xl border border-zinc-200 p-3">
                    <div className="flex flex-wrap items-center justify-between gap-2 text-sm">
                      <div className="font-medium text-zinc-900">
                        {event.channel} · {event.result || '-'}
                      </div>
                      <div className="text-xs text-zinc-500">{event.created_at?.replace('T', ' ').slice(0, 16) || '-'}</div>
                    </div>
                    <div className="mt-1 text-xs text-zinc-500">
                      reason={event.reason_code || '-'} · actor={event.actor || '-'} · ptp={event.ptp_date || '-'} / $
                      {event.ptp_amount.toFixed(2)}
                    </div>
                    {event.note ? <div className="mt-2 text-sm text-zinc-700">{event.note}</div> : null}
                  </div>
                ))
              )}
            </div>
          </div>
        </div>
      )}
    </Drawer>
  )
}
