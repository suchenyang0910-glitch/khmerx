import type { OrderRow } from '@/components/salaryLoan/types'

export default function OrdersPanel(props: {
  status: string
  setStatus: (v: string) => void
  loading: boolean
  orders: OrderRow[]
  onRefresh: () => void
  onOpen: (o: OrderRow) => void
}) {
  return (
    <div className="space-y-3">
      <div className="flex flex-wrap items-center gap-2">
        <select
          value={props.status}
          onChange={(e) => props.setStatus(e.target.value)}
          className="h-9 rounded-lg border border-zinc-200 bg-white px-3 text-sm"
        >
          <option value="">全部状态</option>
          <option value="submitted">submitted</option>
          <option value="factory_pending">factory_pending</option>
          <option value="approved">approved</option>
          <option value="disbursed">disbursed</option>
          <option value="repaying">repaying</option>
          <option value="completed">completed</option>
          <option value="rejected">rejected</option>
        </select>
        <button
          type="button"
          onClick={props.onRefresh}
          className="inline-flex h-9 items-center rounded-lg border border-zinc-200 bg-white px-3 text-sm text-zinc-700 hover:bg-zinc-50"
        >
          刷新
        </button>
      </div>

      <div className="overflow-hidden rounded-2xl border border-zinc-200 bg-white">
        <div className="grid grid-cols-12 gap-2 border-b border-zinc-200 bg-zinc-50 px-3 py-2 text-xs font-medium text-zinc-600">
          <div className="col-span-3">订单</div>
          <div className="col-span-2">金额</div>
          <div className="col-span-2">应还</div>
          <div className="col-span-2">到期</div>
          <div className="col-span-3">状态</div>
        </div>
        {props.loading ? (
          <div className="p-4 text-sm text-zinc-600">加载中…</div>
        ) : props.orders.length === 0 ? (
          <div className="p-4 text-sm text-zinc-600">暂无数据</div>
        ) : (
          props.orders.map((o) => (
            <button
              key={o.id}
              type="button"
              onClick={() => props.onOpen(o)}
              className="grid w-full grid-cols-12 gap-2 border-b border-zinc-100 px-3 py-3 text-left text-sm hover:bg-zinc-50"
            >
              <div className="col-span-3 font-medium text-zinc-900">{o.id.slice(0, 8)}</div>
              <div className="col-span-2 text-zinc-700">${Number(o.principal).toFixed(0)}</div>
              <div className="col-span-2 text-zinc-700">${Number(o.total_due).toFixed(0)}</div>
              <div className="col-span-2 text-zinc-700">{o.due_date || '-'}</div>
              <div className="col-span-3 text-zinc-700">{o.status}</div>
            </button>
          ))
        )}
      </div>
    </div>
  )
}

