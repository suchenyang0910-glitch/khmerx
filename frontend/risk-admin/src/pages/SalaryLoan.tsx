import { useCallback, useEffect, useMemo, useState } from 'react'
import { getErrorMessage, requestJson } from '@/api/http'
import OrdersPanel from '@/components/salaryLoan/OrdersPanel'
import FactoriesPanel from '@/components/salaryLoan/FactoriesPanel'
import CollectionPanel from '@/components/salaryLoan/CollectionPanel'
import CollectionDrawer from '@/components/salaryLoan/CollectionDrawer'
import Drawer from '@/components/Drawer'
import OrderDrawer from '@/components/salaryLoan/OrderDrawer'
import type { CollectionDetail, CollectionRow, FactoryRow, OrderDetail, OrderRow, Tab } from '@/components/salaryLoan/types'

export default function SalaryLoan() {
  const [tab, setTab] = useState<Tab>('orders')

  const [orders, setOrders] = useState<OrderRow[]>([])
  const [factories, setFactories] = useState<FactoryRow[]>([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const [status, setStatus] = useState<string>('')
  const [selected, setSelected] = useState<OrderRow | null>(null)
  const [detail, setDetail] = useState<OrderDetail | null>(null)
  const [drawerLoading, setDrawerLoading] = useState(false)
  const [drawerError, setDrawerError] = useState<string | null>(null)
  const [actionLoading, setActionLoading] = useState(false)
  const [collectionRows, setCollectionRows] = useState<CollectionRow[]>([])
  const [collectionStage, setCollectionStage] = useState<string>('')
  const [collectionStatus, setCollectionStatus] = useState<string>('open')
  const [selectedCollection, setSelectedCollection] = useState<CollectionRow | null>(null)
  const [collectionDetail, setCollectionDetail] = useState<CollectionDetail | null>(null)
  const [collectionLoading, setCollectionLoading] = useState(false)
  const [collectionError, setCollectionError] = useState<string | null>(null)
  const [followChannel, setFollowChannel] = useState('call')
  const [followResult, setFollowResult] = useState('')
  const [followReasonCode, setFollowReasonCode] = useState('')
  const [followNote, setFollowNote] = useState('')
  const [followPtpDate, setFollowPtpDate] = useState('')
  const [followPtpAmount, setFollowPtpAmount] = useState('')
  const [nextFollowUpAt, setNextFollowUpAt] = useState('')

  const [fee, setFee] = useState<string>('0')
  const [interest, setInterest] = useState<string>('0')
  const [disbRef, setDisbRef] = useState<string>('')

  const [newFactoryName, setNewFactoryName] = useState('')
  const [newFactoryIndustry, setNewFactoryIndustry] = useState('factory')
  const [newFactoryLocation, setNewFactoryLocation] = useState('')
  const [newFactoryOwnerType, setNewFactoryOwnerType] = useState('unknown')
  const [newFactorySalaryCycle, setNewFactorySalaryCycle] = useState('monthly')
  const [newFactoryWorkerCount, setNewFactoryWorkerCount] = useState('0')
  const [newFactoryRisk, setNewFactoryRisk] = useState('C')
  const [newFactoryDefaultRate, setNewFactoryDefaultRate] = useState('0')
  const [newFactoryHrContact, setNewFactoryHrContact] = useState('')

  const [selectedFactory, setSelectedFactory] = useState<FactoryRow | null>(null)
  const [editFactory, setEditFactory] = useState<Partial<FactoryRow> | null>(null)

  const tabs = useMemo(
    () => [
      { key: 'orders' as const, label: '订单审核' },
      { key: 'factories' as const, label: '工厂库' },
      { key: 'collections' as const, label: '催收工作台' },
    ],
    [],
  )

  const loadOrders = useCallback(async () => {
    setLoading(true)
    setError(null)
    try {
      const qs = new URLSearchParams()
      if (status) qs.set('status', status)
      qs.set('limit', '100')
      qs.set('offset', '0')
      const rows = await requestJson<OrderRow[]>(`/api/admin/salary-loan/orders?${qs.toString()}`)
      setOrders(rows)
    } catch (e: unknown) {
      setError(getErrorMessage(e))
    } finally {
      setLoading(false)
    }
  }, [status])

  const loadFactories = useCallback(async () => {
    setLoading(true)
    setError(null)
    try {
      const rows = await requestJson<FactoryRow[]>('/api/admin/salary-loan/factories')
      setFactories(rows)
    } catch (e: unknown) {
      setError(getErrorMessage(e))
    } finally {
      setLoading(false)
    }
  }, [])

  const loadCollections = useCallback(async () => {
    setLoading(true)
    setError(null)
    try {
      const qs = new URLSearchParams()
      if (collectionStage) qs.set('stage', collectionStage)
      if (collectionStatus) qs.set('status', collectionStatus)
      qs.set('limit', '100')
      qs.set('offset', '0')
      const rows = await requestJson<CollectionRow[]>(`/api/admin/salary-loan/collections?${qs.toString()}`)
      setCollectionRows(rows)
    } catch (e: unknown) {
      setError(getErrorMessage(e))
    } finally {
      setLoading(false)
    }
  }, [collectionStage, collectionStatus])

  useEffect(() => {
    if (tab === 'orders') void loadOrders()
    if (tab === 'factories') void loadFactories()
    if (tab === 'collections') void loadCollections()
  }, [loadCollections, loadFactories, loadOrders, tab])

  async function openOrder(o: OrderRow) {
    setSelected(o)
    setDetail(null)
    setDrawerLoading(true)
    setDrawerError(null)
    try {
      const d = await requestJson<OrderDetail>(`/api/admin/salary-loan/orders/${o.id}`)
      setDetail(d)
      setFee(String(d.order.fee ?? 0))
      setInterest(String(d.order.interest ?? 0))
      setDisbRef(d.order.disbursement_ref || '')
    } catch (e: unknown) {
      setDrawerError(getErrorMessage(e))
    } finally {
      setDrawerLoading(false)
    }
  }

  async function verifyEmployment() {
    if (!detail?.employment) return
    setActionLoading(true)
    try {
      await requestJson(`/api/admin/salary-loan/employments/${detail.employment.id}/verify`, {
        method: 'POST',
        body: JSON.stringify({ verify_status: 'verified', verify_notes: 'verified' }),
      })
      if (selected) await openOrder(selected)
    } catch (e: unknown) {
      setDrawerError(getErrorMessage(e))
    } finally {
      setActionLoading(false)
    }
  }

  async function decide(decision: 'approve' | 'reject') {
    if (!detail) return
    setActionLoading(true)
    setDrawerError(null)
    try {
      const payload: {
        decision: 'approve' | 'reject'
        approved_principal?: number
        fee?: number
        interest?: number
      } = { decision }
      if (decision === 'approve') {
        payload.approved_principal = detail.order.principal
        payload.fee = Number(fee || '0')
        payload.interest = Number(interest || '0')
      }
      await requestJson(`/api/admin/salary-loan/orders/${detail.order.id}/decision`, {
        method: 'POST',
        body: JSON.stringify(payload),
      })
      await loadOrders()
      if (selected) await openOrder(selected)
    } catch (e: unknown) {
      setDrawerError(getErrorMessage(e))
    } finally {
      setActionLoading(false)
    }
  }

  async function disburse() {
    if (!detail) return
    setActionLoading(true)
    setDrawerError(null)
    try {
      await requestJson(`/api/admin/salary-loan/orders/${detail.order.id}/disburse`, {
        method: 'POST',
        body: JSON.stringify({ disbursement_ref: disbRef }),
      })
      await loadOrders()
      if (selected) await openOrder(selected)
    } catch (e: unknown) {
      setDrawerError(getErrorMessage(e))
    } finally {
      setActionLoading(false)
    }
  }

  async function reviewProof(proofId: string, statusVal: 'accepted' | 'rejected') {
    setActionLoading(true)
    setDrawerError(null)
    try {
      await requestJson(`/api/admin/salary-loan/proofs/${proofId}/review`, {
        method: 'POST',
        body: JSON.stringify({ status: statusVal, note: '' }),
      })
      if (selected) await openOrder(selected)
    } catch (e: unknown) {
      setDrawerError(getErrorMessage(e))
    } finally {
      setActionLoading(false)
    }
  }

  async function createFactory() {
    setLoading(true)
    setError(null)
    try {
      await requestJson('/api/admin/salary-loan/factories', {
        method: 'POST',
        body: JSON.stringify({
          name: newFactoryName,
          industry: newFactoryIndustry,
          location: newFactoryLocation,
          owner_type: newFactoryOwnerType,
          salary_cycle: newFactorySalaryCycle,
          worker_count: Number(newFactoryWorkerCount || '0'),
          risk_level: newFactoryRisk,
          default_rate: Number(newFactoryDefaultRate || '0'),
          hr_contact: newFactoryHrContact,
          is_active: true,
        }),
      })
      setNewFactoryName('')
      setNewFactoryIndustry('factory')
      setNewFactoryLocation('')
      setNewFactoryOwnerType('unknown')
      setNewFactorySalaryCycle('monthly')
      setNewFactoryWorkerCount('0')
      await loadFactories()
    } catch (e: unknown) {
      setError(getErrorMessage(e))
    } finally {
      setLoading(false)
    }
  }

  async function updateFactory() {
    if (!selectedFactory || !editFactory) return
    setLoading(true)
    setError(null)
    try {
      await requestJson(`/api/admin/salary-loan/factories/${selectedFactory.id}`, {
        method: 'PATCH',
        body: JSON.stringify({
          name: editFactory.name,
          industry: editFactory.industry,
          location: editFactory.location,
          owner_type: editFactory.owner_type,
          salary_cycle: editFactory.salary_cycle,
          worker_count: editFactory.worker_count,
          risk_level: editFactory.risk_level,
          default_rate: editFactory.default_rate,
          hr_contact: editFactory.hr_contact,
          is_active: editFactory.is_active,
        }),
      })
      await loadFactories()
      setSelectedFactory(null)
      setEditFactory(null)
    } catch (e: unknown) {
      setError(getErrorMessage(e))
    } finally {
      setLoading(false)
    }
  }

  async function openCollection(row: CollectionRow) {
    setSelectedCollection(row)
    setCollectionDetail(null)
    setCollectionLoading(true)
    setCollectionError(null)
    setFollowChannel('call')
    setFollowResult('')
    setFollowReasonCode('')
    setFollowNote('')
    setFollowPtpDate('')
    setFollowPtpAmount('')
    setNextFollowUpAt('')
    try {
      const data = await requestJson<CollectionDetail>(`/api/admin/salary-loan/collections/${row.id}`)
      setCollectionDetail(data)
    } catch (e: unknown) {
      setCollectionError(getErrorMessage(e))
    } finally {
      setCollectionLoading(false)
    }
  }

  async function createCollectionEvent() {
    if (!selectedCollection) return
    setActionLoading(true)
    setCollectionError(null)
    try {
      const nextFollowUpAtIso = nextFollowUpAt ? new Date(nextFollowUpAt).toISOString() : null
      await requestJson(`/api/admin/salary-loan/collections/${selectedCollection.id}/events`, {
        method: 'POST',
        body: JSON.stringify({
          channel: followChannel,
          result: followResult,
          reason_code: followReasonCode,
          note: followNote,
          ptp_date: followPtpDate || null,
          ptp_amount: Number(followPtpAmount || '0'),
          next_follow_up_at: nextFollowUpAtIso,
        }),
      })
      await loadCollections()
      await openCollection(selectedCollection)
    } catch (e: unknown) {
      setCollectionError(getErrorMessage(e))
    } finally {
      setActionLoading(false)
    }
  }

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <div className="text-base font-semibold">薪资贷审核</div>
        <div className="inline-flex rounded-lg border border-zinc-200 bg-white p-1">
          {tabs.map((t) => (
            <button
              key={t.key}
              type="button"
              onClick={() => setTab(t.key)}
              className={
                tab === t.key
                  ? 'rounded-md bg-zinc-900 px-3 py-1.5 text-sm text-white'
                  : 'rounded-md px-3 py-1.5 text-sm text-zinc-700 hover:bg-zinc-100'
              }
            >
              {t.label}
            </button>
          ))}
        </div>
      </div>

      {error ? <div className="rounded-lg border border-red-200 bg-red-50 px-3 py-2 text-sm text-red-700">{error}</div> : null}

      {tab === 'orders' ? (
        <OrdersPanel
          status={status}
          setStatus={setStatus}
          loading={loading}
          orders={orders}
          onRefresh={() => void loadOrders()}
          onOpen={(o) => void openOrder(o)}
        />
      ) : tab === 'factories' ? (
        <FactoriesPanel
          loading={loading}
          factories={factories}
          newFactoryName={newFactoryName}
          setNewFactoryName={setNewFactoryName}
          newFactoryIndustry={newFactoryIndustry}
          setNewFactoryIndustry={setNewFactoryIndustry}
          newFactoryLocation={newFactoryLocation}
          setNewFactoryLocation={setNewFactoryLocation}
          newFactoryOwnerType={newFactoryOwnerType}
          setNewFactoryOwnerType={setNewFactoryOwnerType}
          newFactorySalaryCycle={newFactorySalaryCycle}
          setNewFactorySalaryCycle={setNewFactorySalaryCycle}
          newFactoryWorkerCount={newFactoryWorkerCount}
          setNewFactoryWorkerCount={setNewFactoryWorkerCount}
          newFactoryRisk={newFactoryRisk}
          setNewFactoryRisk={setNewFactoryRisk}
          newFactoryDefaultRate={newFactoryDefaultRate}
          setNewFactoryDefaultRate={setNewFactoryDefaultRate}
          newFactoryHrContact={newFactoryHrContact}
          setNewFactoryHrContact={setNewFactoryHrContact}
          onCreate={() => void createFactory()}
          onOpenFactory={(f) => {
            setSelectedFactory(f)
            setEditFactory({ ...f })
          }}
        />
      ) : (
        <CollectionPanel
          stage={collectionStage}
          setStage={setCollectionStage}
          status={collectionStatus}
          setStatus={setCollectionStatus}
          loading={loading}
          rows={collectionRows}
          onRefresh={() => void loadCollections()}
          onOpen={(row) => void openCollection(row)}
        />
      )}

      <Drawer
        open={!!selectedFactory && !!editFactory}
        title={selectedFactory ? `编辑工厂：${selectedFactory.name}` : '编辑工厂'}
        onClose={() => {
          setSelectedFactory(null)
          setEditFactory(null)
        }}
      >
        {editFactory ? (
          <div className="space-y-3">
            <div className="grid grid-cols-1 gap-3 md:grid-cols-2">
              <div>
                <div className="text-xs font-medium text-zinc-700">名称</div>
                <input
                  value={editFactory.name || ''}
                  onChange={(e) => setEditFactory({ ...editFactory, name: e.target.value })}
                  className="mt-1 h-9 w-full rounded-lg border border-zinc-200 px-3 text-sm"
                />
              </div>
              <div>
                <div className="text-xs font-medium text-zinc-700">行业</div>
                <input
                  value={editFactory.industry || ''}
                  onChange={(e) => setEditFactory({ ...editFactory, industry: e.target.value })}
                  className="mt-1 h-9 w-full rounded-lg border border-zinc-200 px-3 text-sm"
                />
              </div>
              <div>
                <div className="text-xs font-medium text-zinc-700">地点</div>
                <input
                  value={editFactory.location || ''}
                  onChange={(e) => setEditFactory({ ...editFactory, location: e.target.value })}
                  className="mt-1 h-9 w-full rounded-lg border border-zinc-200 px-3 text-sm"
                />
              </div>
              <div>
                <div className="text-xs font-medium text-zinc-700">所有制</div>
                <select
                  value={editFactory.owner_type || 'unknown'}
                  onChange={(e) => setEditFactory({ ...editFactory, owner_type: e.target.value })}
                  className="mt-1 h-9 w-full rounded-lg border border-zinc-200 bg-white px-3 text-sm"
                >
                  <option value="unknown">unknown</option>
                  <option value="private">private</option>
                  <option value="state">state</option>
                  <option value="foreign">foreign</option>
                </select>
              </div>
              <div>
                <div className="text-xs font-medium text-zinc-700">发薪周期</div>
                <select
                  value={editFactory.salary_cycle || 'monthly'}
                  onChange={(e) => setEditFactory({ ...editFactory, salary_cycle: e.target.value })}
                  className="mt-1 h-9 w-full rounded-lg border border-zinc-200 bg-white px-3 text-sm"
                >
                  <option value="monthly">monthly</option>
                  <option value="biweekly">biweekly</option>
                  <option value="weekly">weekly</option>
                  <option value="unknown">unknown</option>
                </select>
              </div>
              <div>
                <div className="text-xs font-medium text-zinc-700">工人数</div>
                <input
                  type="number"
                  value={String(editFactory.worker_count ?? 0)}
                  onChange={(e) => setEditFactory({ ...editFactory, worker_count: Number(e.target.value || '0') })}
                  className="mt-1 h-9 w-full rounded-lg border border-zinc-200 px-3 text-sm"
                />
              </div>
              <div>
                <div className="text-xs font-medium text-zinc-700">风险等级</div>
                <select
                  value={editFactory.risk_level || 'C'}
                  onChange={(e) => setEditFactory({ ...editFactory, risk_level: e.target.value })}
                  className="mt-1 h-9 w-full rounded-lg border border-zinc-200 bg-white px-3 text-sm"
                >
                  <option value="A">A</option>
                  <option value="B">B</option>
                  <option value="C">C</option>
                  <option value="D">D</option>
                </select>
              </div>
              <div>
                <div className="text-xs font-medium text-zinc-700">默认费率</div>
                <input
                  type="number"
                  step="0.0001"
                  value={String(editFactory.default_rate ?? 0)}
                  onChange={(e) => setEditFactory({ ...editFactory, default_rate: Number(e.target.value || '0') })}
                  className="mt-1 h-9 w-full rounded-lg border border-zinc-200 px-3 text-sm"
                />
              </div>
              <div className="md:col-span-2">
                <div className="text-xs font-medium text-zinc-700">HR 联系方式</div>
                <input
                  value={editFactory.hr_contact || ''}
                  onChange={(e) => setEditFactory({ ...editFactory, hr_contact: e.target.value })}
                  className="mt-1 h-9 w-full rounded-lg border border-zinc-200 px-3 text-sm"
                />
              </div>
              <label className="inline-flex items-center gap-2 text-sm text-zinc-700">
                <input
                  type="checkbox"
                  checked={Boolean(editFactory.is_active)}
                  onChange={(e) => setEditFactory({ ...editFactory, is_active: e.target.checked })}
                />
                启用
              </label>
            </div>

            <div className="flex gap-2">
              <button
                type="button"
                disabled={loading}
                onClick={() => void updateFactory()}
                className="inline-flex h-9 items-center justify-center rounded-lg bg-zinc-900 px-4 text-sm font-medium text-white disabled:opacity-50"
              >
                保存
              </button>
              <button
                type="button"
                disabled={loading}
                onClick={() => {
                  setSelectedFactory(null)
                  setEditFactory(null)
                }}
                className="inline-flex h-9 items-center justify-center rounded-lg border border-zinc-200 bg-white px-4 text-sm text-zinc-700 disabled:opacity-50"
              >
                取消
              </button>
            </div>
          </div>
        ) : null}
      </Drawer>

      <OrderDrawer
        open={!!selected}
        selected={selected}
        detail={detail}
        loading={drawerLoading}
        error={drawerError}
        fee={fee}
        setFee={setFee}
        interest={interest}
        setInterest={setInterest}
        disbRef={disbRef}
        setDisbRef={setDisbRef}
        actionLoading={actionLoading}
        onClose={() => {
          setSelected(null)
          setDetail(null)
          setDrawerError(null)
        }}
        onVerifyEmployment={() => void verifyEmployment()}
        onDecide={(d) => void decide(d)}
        onDisburse={() => void disburse()}
        onReviewProof={(id, s) => void reviewProof(id, s)}
      />

      <CollectionDrawer
        open={!!selectedCollection}
        selected={selectedCollection}
        detail={collectionDetail}
        loading={collectionLoading}
        error={collectionError}
        actionLoading={actionLoading}
        followChannel={followChannel}
        setFollowChannel={setFollowChannel}
        followResult={followResult}
        setFollowResult={setFollowResult}
        followReasonCode={followReasonCode}
        setFollowReasonCode={setFollowReasonCode}
        followNote={followNote}
        setFollowNote={setFollowNote}
        followPtpDate={followPtpDate}
        setFollowPtpDate={setFollowPtpDate}
        followPtpAmount={followPtpAmount}
        setFollowPtpAmount={setFollowPtpAmount}
        nextFollowUpAt={nextFollowUpAt}
        setNextFollowUpAt={setNextFollowUpAt}
        onClose={() => {
          setSelectedCollection(null)
          setCollectionDetail(null)
          setCollectionError(null)
        }}
        onCreateEvent={() => void createCollectionEvent()}
      />
    </div>
  )
}
