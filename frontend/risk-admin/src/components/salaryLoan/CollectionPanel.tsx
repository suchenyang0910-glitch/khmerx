import type { CollectionRow } from '@/components/salaryLoan/types'

export default function CollectionPanel(props: {
  stage: string
  setStage: (v: string) => void
  status: string
  setStatus: (v: string) => void
  loading: boolean
  rows: CollectionRow[]
  onRefresh: () => void
  onOpen: (row: CollectionRow) => void
}) {
  return (
    <div className="space-y-3">
      <div className="flex flex-wrap items-center gap-2">
        <select
          value={props.stage}
          onChange={(e) => props.setStage(e.target.value)}
          className="h-9 rounded-lg border border-zinc-200 bg-white px-3 text-sm"
        >
          <option value="">全部阶段</option>
          <option value="pre">pre</option>
          <option value="early">early</option>
          <option value="mid">mid</option>
          <option value="late">late</option>
        </select>
        <select
          value={props.status}
          onChange={(e) => props.setStatus(e.target.value)}
          className="h-9 rounded-lg border border-zinc-200 bg-white px-3 text-sm"
        >
          <option value="">全部状态</option>
          <option value="open">open</option>
          <option value="closed">closed</option>
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
          <div className="col-span-2">订单</div>
          <div className="col-span-2">企业</div>
          <div className="col-span-1">DPD</div>
          <div className="col-span-1">阶段</div>
          <div className="col-span-2">应还</div>
          <div className="col-span-2">跟进人</div>
          <div className="col-span-2">下次跟进</div>
        </div>
        {props.loading ? (
          <div className="p-4 text-sm text-zinc-600">加载中…</div>
        ) : props.rows.length === 0 ? (
          <div className="p-4 text-sm text-zinc-600">暂无催收案件</div>
        ) : (
          props.rows.map((row) => (
            <button
              key={row.id}
              type="button"
              onClick={() => props.onOpen(row)}
              className="grid w-full grid-cols-12 gap-2 border-b border-zinc-100 px-3 py-3 text-left text-sm hover:bg-zinc-50"
            >
              <div className="col-span-2 font-medium text-zinc-900">{row.order_id.slice(0, 8)}</div>
              <div className="col-span-2 text-zinc-700">{row.factory_name || '-'}</div>
              <div className="col-span-1 text-zinc-700">{row.dpd}</div>
              <div className="col-span-1 text-zinc-700">{row.stage}</div>
              <div className="col-span-2 text-zinc-700">${row.total_due.toFixed(2)}</div>
              <div className="col-span-2 text-zinc-700">{row.assignee || '-'}</div>
              <div className="col-span-2 text-zinc-700">{row.next_follow_up_at?.slice(0, 16).replace('T', ' ') || '-'}</div>
            </button>
          ))
        )}
      </div>
    </div>
  )
}
