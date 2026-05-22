import Drawer from '@/components/Drawer'
import type { OrderDetail, OrderRow } from '@/components/salaryLoan/types'

export default function OrderDrawer(props: {
  selected: OrderRow | null
  detail: OrderDetail | null
  open: boolean
  loading: boolean
  error: string | null
  fee: string
  setFee: (v: string) => void
  interest: string
  setInterest: (v: string) => void
  disbRef: string
  setDisbRef: (v: string) => void
  actionLoading: boolean
  onClose: () => void
  onVerifyEmployment: () => void
  onDecide: (decision: 'approve' | 'reject') => void
  onDisburse: () => void
  onReviewProof: (proofId: string, status: 'accepted' | 'rejected') => void
}) {
  return (
    <Drawer
      open={props.open}
      title={props.selected ? `订单 ${props.selected.id.slice(0, 8)}` : ''}
      onClose={props.onClose}
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
          <div className="rounded-2xl border border-zinc-200 bg-white p-4">
            <div className="grid grid-cols-2 gap-3 text-sm">
              <div>
                <div className="text-xs text-zinc-500">状态</div>
                <div className="font-medium text-zinc-900">{props.detail.order.status}</div>
              </div>
              <div>
                <div className="text-xs text-zinc-500">风险分</div>
                <div className="font-medium text-zinc-900">{props.detail.order.risk_score ?? '-'}</div>
              </div>
              <div>
                <div className="text-xs text-zinc-500">本金</div>
                <div className="font-medium text-zinc-900">${Number(props.detail.order.principal).toFixed(2)}</div>
              </div>
              <div>
                <div className="text-xs text-zinc-500">应还</div>
                <div className="font-medium text-zinc-900">
                  ${Number(props.detail.order.principal + props.detail.order.fee + props.detail.order.interest).toFixed(2)}
                </div>
              </div>
            </div>
            {props.detail.factory ? (
              <div className="mt-3 rounded-xl bg-zinc-50 p-3 text-sm">
                <div className="font-medium text-zinc-900">{props.detail.factory.name}</div>
                <div className="mt-1 text-xs text-zinc-500">
                  {props.detail.factory.location} · risk {props.detail.factory.risk_level}
                </div>
              </div>
            ) : null}
            {props.detail.employment ? (
              <div className="mt-3 rounded-xl bg-zinc-50 p-3 text-sm">
                <div className="font-medium text-zinc-900">就业信息</div>
                <div className="mt-1 text-xs text-zinc-500">工号 {props.detail.employment.employee_no || '-'}</div>
                <div className="mt-1 text-xs text-zinc-500">
                  {props.detail.employment.pay_cycle} · {props.detail.employment.pay_method} · {props.detail.employment.verify_status}
                </div>
                {props.detail.employment.verify_status !== 'verified' ? (
                  <button
                    type="button"
                    disabled={props.actionLoading}
                    onClick={props.onVerifyEmployment}
                    className="mt-2 inline-flex h-9 items-center rounded-lg bg-zinc-900 px-3 text-sm font-medium text-white disabled:opacity-50"
                  >
                    一键通过在职验证
                  </button>
                ) : null}
              </div>
            ) : null}
          </div>

          {props.detail.order.status === 'approved' ? (
            <div className="rounded-2xl border border-zinc-200 bg-white p-4">
              <div className="text-sm font-semibold text-zinc-900">放款</div>
              <div className="mt-3 grid grid-cols-1 gap-3 md:grid-cols-2">
                <input
                  value={props.disbRef}
                  onChange={(e) => props.setDisbRef(e.target.value)}
                  placeholder="转账流水/参考号"
                  className="h-9 rounded-lg border border-zinc-200 px-3 text-sm"
                />
                <button
                  type="button"
                  disabled={props.actionLoading}
                  onClick={props.onDisburse}
                  className="inline-flex h-9 items-center justify-center rounded-lg bg-zinc-900 px-3 text-sm font-medium text-white disabled:opacity-50"
                >
                  放款确认
                </button>
              </div>
            </div>
          ) : null}

          {['submitted', 'factory_pending', 'manual_review'].includes(props.detail.order.status) ? (
            <div className="rounded-2xl border border-zinc-200 bg-white p-4">
              <div className="text-sm font-semibold text-zinc-900">审核决策</div>
              <div className="mt-3 grid grid-cols-1 gap-3 md:grid-cols-3">
                <input
                  value={props.fee}
                  onChange={(e) => props.setFee(e.target.value)}
                  className="h-9 rounded-lg border border-zinc-200 px-3 text-sm"
                  placeholder="fee"
                />
                <input
                  value={props.interest}
                  onChange={(e) => props.setInterest(e.target.value)}
                  className="h-9 rounded-lg border border-zinc-200 px-3 text-sm"
                  placeholder="interest"
                />
                <div className="flex gap-2">
                  <button
                    type="button"
                    disabled={props.actionLoading}
                    onClick={() => props.onDecide('approve')}
                    className="inline-flex h-9 flex-1 items-center justify-center rounded-lg bg-zinc-900 px-3 text-sm font-medium text-white disabled:opacity-50"
                  >
                    通过
                  </button>
                  <button
                    type="button"
                    disabled={props.actionLoading}
                    onClick={() => props.onDecide('reject')}
                    className="inline-flex h-9 flex-1 items-center justify-center rounded-lg border border-zinc-200 bg-white px-3 text-sm font-medium text-zinc-700 hover:bg-zinc-50 disabled:opacity-50"
                  >
                    拒绝
                  </button>
                </div>
              </div>
            </div>
          ) : null}

          <div className="rounded-2xl border border-zinc-200 bg-white p-4">
            <div className="text-sm font-semibold text-zinc-900">还款凭证</div>
            <div className="mt-3 space-y-2">
              {props.detail.proofs.length === 0 ? (
                <div className="text-sm text-zinc-600">暂无</div>
              ) : (
                props.detail.proofs.map((p) => (
                  <div key={p.id} className="flex items-start justify-between gap-3 rounded-xl border border-zinc-200 p-3">
                    <div className="min-w-0">
                      <div className="truncate text-sm font-medium text-zinc-900">
                        ${Number(p.amount).toFixed(2)} · {p.status}
                      </div>
                      <div className="mt-1 truncate text-xs text-zinc-500">{p.file_path}</div>
                      {p.note ? <div className="mt-1 text-xs text-zinc-500">{p.note}</div> : null}
                    </div>
                    {p.status === 'pending' ? (
                      <div className="flex shrink-0 gap-2">
                        <button
                          type="button"
                          disabled={props.actionLoading}
                          onClick={() => props.onReviewProof(p.id, 'accepted')}
                          className="inline-flex h-9 items-center rounded-lg bg-zinc-900 px-3 text-sm font-medium text-white disabled:opacity-50"
                        >
                          通过
                        </button>
                        <button
                          type="button"
                          disabled={props.actionLoading}
                          onClick={() => props.onReviewProof(p.id, 'rejected')}
                          className="inline-flex h-9 items-center rounded-lg border border-zinc-200 bg-white px-3 text-sm font-medium text-zinc-700 hover:bg-zinc-50 disabled:opacity-50"
                        >
                          驳回
                        </button>
                      </div>
                    ) : null}
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

