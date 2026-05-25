import type { FactoryRow } from '@/components/salaryLoan/types'

export default function FactoriesPanel(props: {
  loading: boolean
  factories: FactoryRow[]
  newFactoryName: string
  setNewFactoryName: (v: string) => void
  newFactoryIndustry: string
  setNewFactoryIndustry: (v: string) => void
  newFactoryLocation: string
  setNewFactoryLocation: (v: string) => void
  newFactoryOwnerType: string
  setNewFactoryOwnerType: (v: string) => void
  newFactorySalaryCycle: string
  setNewFactorySalaryCycle: (v: string) => void
  newFactoryWorkerCount: string
  setNewFactoryWorkerCount: (v: string) => void
  newFactoryRisk: string
  setNewFactoryRisk: (v: string) => void
  newFactoryDefaultRate: string
  setNewFactoryDefaultRate: (v: string) => void
  newFactoryHrContact: string
  setNewFactoryHrContact: (v: string) => void
  onCreate: () => void
  onOpenFactory: (f: FactoryRow) => void
}) {
  return (
    <div className="space-y-3">
      <div className="rounded-2xl border border-zinc-200 bg-white p-4">
        <div className="text-sm font-semibold text-zinc-900">新增企业（工厂）</div>
        <div className="mt-3 grid grid-cols-1 gap-3 md:grid-cols-3">
          <input
            value={props.newFactoryName}
            onChange={(e) => props.setNewFactoryName(e.target.value)}
            placeholder="企业名称"
            className="h-9 rounded-lg border border-zinc-200 px-3 text-sm"
          />
          <input
            value={props.newFactoryIndustry}
            onChange={(e) => props.setNewFactoryIndustry(e.target.value)}
            placeholder="行业"
            className="h-9 rounded-lg border border-zinc-200 px-3 text-sm"
          />
          <input
            value={props.newFactoryLocation}
            onChange={(e) => props.setNewFactoryLocation(e.target.value)}
            placeholder="地点"
            className="h-9 rounded-lg border border-zinc-200 px-3 text-sm"
          />
          <select
            value={props.newFactoryOwnerType}
            onChange={(e) => props.setNewFactoryOwnerType(e.target.value)}
            className="h-9 rounded-lg border border-zinc-200 bg-white px-3 text-sm"
          >
            <option value="unknown">所有制：unknown</option>
            <option value="private">所有制：private</option>
            <option value="state">所有制：state</option>
            <option value="foreign">所有制：foreign</option>
          </select>
          <select
            value={props.newFactorySalaryCycle}
            onChange={(e) => props.setNewFactorySalaryCycle(e.target.value)}
            className="h-9 rounded-lg border border-zinc-200 bg-white px-3 text-sm"
          >
            <option value="monthly">发薪：monthly</option>
            <option value="biweekly">发薪：biweekly</option>
            <option value="weekly">发薪：weekly</option>
            <option value="unknown">发薪：unknown</option>
          </select>
          <input
            type="number"
            value={props.newFactoryWorkerCount}
            onChange={(e) => props.setNewFactoryWorkerCount(e.target.value)}
            placeholder="工人数"
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
          <input
            type="number"
            step="0.0001"
            value={props.newFactoryDefaultRate}
            onChange={(e) => props.setNewFactoryDefaultRate(e.target.value)}
            placeholder="默认费率"
            className="h-9 rounded-lg border border-zinc-200 px-3 text-sm"
          />
          <input
            value={props.newFactoryHrContact}
            onChange={(e) => props.setNewFactoryHrContact(e.target.value)}
            placeholder="HR 联系方式"
            className="h-9 rounded-lg border border-zinc-200 px-3 text-sm"
          />
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
          <div className="col-span-4">企业</div>
          <div className="col-span-2">地点</div>
          <div className="col-span-2">发薪</div>
          <div className="col-span-1">风险</div>
          <div className="col-span-1">人数</div>
          <div className="col-span-2">状态</div>
        </div>
        {props.loading ? (
          <div className="p-4 text-sm text-zinc-600">加载中…</div>
        ) : props.factories.length === 0 ? (
          <div className="p-4 text-sm text-zinc-600">暂无数据</div>
        ) : (
          props.factories.map((f) => (
            <button
              key={f.id}
              type="button"
              onClick={() => props.onOpenFactory(f)}
              className="grid w-full grid-cols-12 gap-2 border-b border-zinc-100 px-3 py-3 text-left text-sm hover:bg-zinc-50"
            >
              <div className="col-span-4 font-medium text-zinc-900">{f.name}</div>
              <div className="col-span-2 text-zinc-700">{f.location}</div>
              <div className="col-span-2 text-zinc-700">{f.salary_cycle || '-'}</div>
              <div className="col-span-1 text-zinc-700">{f.risk_level}</div>
              <div className="col-span-1 text-zinc-700">{typeof f.worker_count === 'number' ? f.worker_count : '-'}</div>
              <div className="col-span-2 text-zinc-700">{f.is_active ? 'active' : 'disabled'}</div>
            </button>
          ))
        )}
      </div>
    </div>
  )
}
