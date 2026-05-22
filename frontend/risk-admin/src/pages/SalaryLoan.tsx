import { useCallback, useEffect, useMemo, useState } from 'react'
import { getErrorMessage, requestJson } from '@/api/http'
import OrdersPanel from '@/components/salaryLoan/OrdersPanel'
import FactoriesPanel from '@/components/salaryLoan/FactoriesPanel'
import OrderDrawer from '@/components/salaryLoan/OrderDrawer'
import type { FactoryRow, OrderDetail, OrderRow, Tab } from '@/components/salaryLoan/types'

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

  const [fee, setFee] = useState<string>('0')
  const [interest, setInterest] = useState<string>('0')
  const [disbRef, setDisbRef] = useState<string>('')

  const [newFactoryName, setNewFactoryName] = useState('')
  const [newFactoryLocation, setNewFactoryLocation] = useState('')
  const [newFactoryRisk, setNewFactoryRisk] = useState('C')

  const tabs = useMemo(
    () => [
      { key: 'orders' as const, label: '订单审核' },
      { key: 'factories' as const, label: '工厂库' },
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

  useEffect(() => {
    if (tab === 'orders') void loadOrders()
    if (tab === 'factories') void loadFactories()
  }, [loadFactories, loadOrders, tab])

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
          location: newFactoryLocation,
          risk_level: newFactoryRisk,
          is_active: true,
        }),
      })
      setNewFactoryName('')
      setNewFactoryLocation('')
      await loadFactories()
    } catch (e: unknown) {
      setError(getErrorMessage(e))
    } finally {
      setLoading(false)
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
      ) : (
        <FactoriesPanel
          loading={loading}
          factories={factories}
          newFactoryName={newFactoryName}
          setNewFactoryName={setNewFactoryName}
          newFactoryLocation={newFactoryLocation}
          setNewFactoryLocation={setNewFactoryLocation}
          newFactoryRisk={newFactoryRisk}
          setNewFactoryRisk={setNewFactoryRisk}
          onCreate={() => void createFactory()}
        />
      )}

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
    </div>
  )
}
