import type { FactoryRow } from '@/components/salaryLoan/types'

export default function FactoriesPanel(props: {
  loading: boolean
  factories: FactoryRow[]
  newFactoryName: string
  setNewFactoryName: (v: string) => void
  newFactoryLocation: string
  setNewFactoryLocation: (v: string) => void
  newFactoryRisk: string
  setNewFactoryRisk: (v: string) => void
  onCreate: () => void
}) {
  return (
    <div className="space-y-3">
      <div className="rounded-2xl border border-zinc-200 bg-white p-4">
        <div className="text-sm font-semibold text-zinc-900">新增工厂</div>
        <div className="mt-3 grid grid-cols-1 gap-3 md:grid-cols-4">
          <input
            value={props.newFactoryName}
            onChange={(e) => props.setNewFactoryName(e.target.value)}
            placeholder="工厂名称"
            className="h-9 rounded-lg border border-zinc-200 px-3 text-sm"
          />
          <input
            value={props.newFactoryLocation}
            onChange={(e) => props.setNewFactoryLocation(e.target.value)}
            placeholder="地点"
            className="h-9 rounded-lg border border-zinc-200 px-3 text-sm"
          />
          <select
            value={props.newFactoryRisk}
            onChange={(e) => props.setNewFactoryRisk(e.target.value)}
            className="h-9 rounded-lg border border-zinc-200 bg-white px-3 text-sm"
          >
            <option value="A">A</option>
            <option value="B">B</option>
            <option value="C">C</option>
            <option value="D">D</option>
          </select>
          <button
            type="button"
            disabled={props.loading || !props.newFactoryName.trim()}
            onClick={props.onCreate}
            className="inline-flex h-9 items-center justify-center rounded-lg bg-zinc-900 px-3 text-sm font-medium text-white disabled:opacity-50"
          >
            保存
          </button>
        </div>
      </div>

      <div className="overflow-hidden rounded-2xl border border-zinc-200 bg-white">
        <div className="grid grid-cols-12 gap-2 border-b border-zinc-200 bg-zinc-50 px-3 py-2 text-xs font-medium text-zinc-600">
          <div className="col-span-6">工厂</div>
          <div className="col-span-3">地点</div>
          <div className="col-span-1">风险</div>
          <div className="col-span-2">状态</div>
        </div>
        {props.loading ? (
          <div className="p-4 text-sm text-zinc-600">加载中…</div>
        ) : props.factories.length === 0 ? (
          <div className="p-4 text-sm text-zinc-600">暂无数据</div>
        ) : (
          props.factories.map((f) => (
            <div key={f.id} className="grid grid-cols-12 gap-2 border-b border-zinc-100 px-3 py-3 text-sm">
              <div className="col-span-6 font-medium text-zinc-900">{f.name}</div>
              <div className="col-span-3 text-zinc-700">{f.location}</div>
              <div className="col-span-1 text-zinc-700">{f.risk_level}</div>
              <div className="col-span-2 text-zinc-700">{f.is_active ? 'active' : 'disabled'}</div>
            </div>
          ))
        )}
      </div>
    </div>
  )
}

