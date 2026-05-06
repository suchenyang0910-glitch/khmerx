import { useCallback, useEffect, useMemo, useState } from "react"
import { useParams, useNavigate } from "react-router-dom"
import Card from "@/components/ui/Card"
import Button from "@/components/ui/Button"
import Badge from "@/components/ui/Badge"
import NextStepCard from "@/components/trade/NextStepCard"
import TradeStepper from "@/components/trade/TradeStepper"
import RepaymentPlan from "@/components/trade/RepaymentPlan"
import ProofSheet from "@/components/trade/ProofSheet"
import DisputeSection from "@/components/trade/DisputeSection"
import { stepIndex } from "@/components/trade/tradeUtils"
import { api, apiV1 } from "@/api/client"
import type { Dispute } from "@/api/types"
import { useAuthStore } from "@/stores/authStore"
import { ArrowLeft } from "lucide-react"
import { errorMessage } from "@/utils/errors"

type ScheduleV1 = {
  id: string
  period: number
  due_at?: string | null
  principal: number
  interest: number
  total: number
  status: "pending" | "paid_pending" | "paid" | "overdue"
  paid_at?: string | null
  proof_url?: string
}

type TradeV1 = {
  id: string
  offer_id: string
  borrower_id: string
  lender_id: string
  amount: number
  term_days: number
  rate_percent: number
  interest: number
  received_amount: number
  repay_amount: number
  status: string
  lend_deadline?: string | null
  proof_url_from_lender?: string
  proof_url_from_borrower?: string
  borrower_aba_account?: string
  borrower_aba_name?: string
  repayment_schedules: ScheduleV1[]
}

export default function TradeDetail() {
  const { tradeId } = useParams()
  const nav = useNavigate()
  const user = useAuthStore((s) => s.user)
  const [trade, setTrade] = useState<TradeV1 | null>(null)
  const [schedules, setSchedules] = useState<ScheduleV1[]>([])
  const [disputes, setDisputes] = useState<Dispute[]>([])
  const [loading, setLoading] = useState(false)
  const [now, setNow] = useState(Date.now())

  const [proofOpen, setProofOpen] = useState(false)
  const [proofUrl, setProofUrl] = useState("")
  const [proofScheduleId, setProofScheduleId] = useState<string>("")
  const [proofAmount, setProofAmount] = useState<number>(0)
  const [proofTitle, setProofTitle] = useState("")
  const [submitting, setSubmitting] = useState(false)
  const [err, setErr] = useState<string | null>(null)

  useEffect(() => {
    const t = setInterval(() => setNow(Date.now()), 1000)
    return () => clearInterval(t)
  }, [])

  const refresh = useCallback(async () => {
    if (!user || !tradeId) return
    setLoading(true)
    setErr(null)
    try {
      const tr = await apiV1.get<{ ok: boolean; data: TradeV1 }>(`/trades/${tradeId}`)
      setTrade(tr.data.data)
      setSchedules(tr.data.data.repayment_schedules || [])
      const ds = await apiV1.get<{ ok: boolean; data: Dispute[] }>("/disputes", { params: { trade_id: tradeId } })
      setDisputes(ds.data.data || [])
    } catch (e: unknown) {
      setErr(errorMessage(e, "加载失败"))
    } finally {
      setLoading(false)
    }
  }, [tradeId, user])

  useEffect(() => {
    refresh()
  }, [refresh])

  const role = useMemo<"lender" | "borrower" | "unknown">(() => {
    if (!user || !trade) return "unknown"
    if (trade.lender_id === user.id) return "lender"
    if (trade.borrower_id === user.id) return "borrower"
    return "unknown"
  }, [trade, user])

  void now

  const nextTip = useMemo(() => {
    if (!trade) return { title: "", desc: "" }
    if (trade.status === "matched") {
      return role === "lender"
        ? { title: "当前：等待打款", desc: "下一步：请在 24 小时内转账并上传凭证" }
        : { title: "当前：等待放款", desc: "下一步：等待放款人转账并上传凭证" }
    }
    if (trade.status === "lend_confirmed") {
      return role === "borrower"
        ? { title: "当前：已打款", desc: "下一步：请确认收款（可选上传收款凭证）" }
        : { title: "当前：已上传凭证", desc: "下一步：等待借款人确认收款" }
    }
    if (trade.status === "repayment_confirmed") {
      return role === "borrower"
        ? { title: "当前：已确认收款", desc: "下一步：开始还款（上传还款凭证）" }
        : { title: "当前：已确认收款", desc: "下一步：等待借款人还款" }
    }
    if (trade.status === "repaying") {
      if (role === "borrower") {
        const next = schedules.find((s) => s.status === "pending" || s.status === "overdue")
        return next
          ? { title: `当前：还款中（第 ${next.period} 期）`, desc: `下一步：上传还款凭证（到期日：${next.due_at ? new Date(next.due_at).toLocaleDateString() : "-"}）` }
          : { title: "当前：还款中", desc: "下一步：等待放款人确认" }
      }
      const pendingConfirm = schedules.find((s) => s.status === "paid_pending")
      return pendingConfirm
        ? { title: "当前：待确认还款", desc: `下一步：确认第 ${pendingConfirm.period} 期回款` }
        : { title: "当前：还款中", desc: "下一步：等待借款人操作" }
    }
    if (trade.status === "completed") return { title: "已完成", desc: "交易结束，感谢按流程完成" }
    if (trade.status === "dispute") return { title: "争议处理中", desc: "已进入仲裁流程，请在下方查看/补充证据" }
    return { title: `状态：${trade.status}`, desc: "请查看详情" }
  }, [role, schedules, trade])

  const actions = useMemo(() => {
    if (!trade || !user) return [] as Array<{ key: string; label: string; onClick: () => void }>

    if (trade.status === "matched" && role === "lender") {
      return [{
        key: "lend",
        label: "上传打款凭证",
        onClick: () => {
          setProofTitle("上传打款凭证")
          setProofScheduleId("")
          setProofUrl("")
          setProofAmount(trade.received_amount || trade.amount)
          setProofOpen(true)
        },
      }]
    }
    if (trade.status === "lend_confirmed" && role === "borrower") {
      return [{
        key: "recv",
        label: "确认收款",
        onClick: async () => {
          setSubmitting(true)
          setErr(null)
          try {
            await apiV1.post(`/trades/${trade.id}/confirm-receive`, { confirmed: true })
            await refresh()
          } catch (e: unknown) {
            setErr(errorMessage(e, "确认失败"))
          } finally {
            setSubmitting(false)
          }
        },
      }]
    }
    if ((trade.status === "repayment_confirmed" || trade.status === "repaying") && role === "borrower") {
      const next = schedules.find((s) => s.status === "pending" || s.status === "overdue")
      if (next) {
        return [{
          key: "repay",
          label: `上传第 ${next.period} 期还款凭证`,
          onClick: () => {
            setProofTitle(`上传第 ${next.period} 期还款凭证`)
            setProofScheduleId(next.id)
            setProofUrl("")
            setProofAmount(next.total)
            setProofOpen(true)
          },
        }]
      }
    }
    if (trade.status === "repaying" && role === "lender") {
      const pending = schedules.find((s) => s.status === "paid_pending")
      if (pending) {
        return [{ key: "confirm", label: `确认第 ${pending.period} 期回款`, onClick: async () => {
          setSubmitting(true)
          setErr(null)
          try {
            await apiV1.post(`/trades/${trade.id}/confirm-repayment`, { schedule_id: pending.id, confirmed: true })
            await refresh()
          } catch (e: unknown) {
            setErr(errorMessage(e, "确认失败"))
          } finally {
            setSubmitting(false)
          }
        } }]
      }
    }
    return []
  }, [refresh, role, schedules, trade, user])

  if (loading && !trade) {
    return <div className="h-24 animate-pulse rounded-2xl bg-white" />
  }

  if (err && !trade) {
    return (
      <Card className="p-4">
        <div className="text-sm font-semibold text-zinc-900">无法加载交易</div>
        <div className="mt-2 text-sm text-zinc-600">{err}</div>
      </Card>
    )
  }

  if (!trade) return null

  const idx = stepIndex(trade.status)

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <button onClick={() => nav(-1)} className="inline-flex items-center gap-2 text-sm text-zinc-600">
          <ArrowLeft className="h-4 w-4" /> 返回
        </button>
        <Badge tone={trade.status === "completed" ? "green" : trade.status === "dispute" ? "yellow" : "blue"}>{trade.status}</Badge>
      </div>

      <TradeStepper index={idx} />

      <NextStepCard
        title={nextTip.title}
        desc={nextTip.desc}
        deadline={trade.status === "matched" ? trade.lend_deadline : null}
      />

      <Card className="p-4">
        <div className="flex items-center justify-between">
          <div className="text-sm font-semibold text-zinc-900">交易信息</div>
          <div className="text-xs text-zinc-500">{role === "lender" ? "你是放款人" : "你是借款人"}</div>
        </div>
        <div className="mt-2 grid grid-cols-2 gap-2 text-sm">
          <div className="rounded-2xl bg-zinc-50 p-3">
            <div className="text-xs text-zinc-500">金额</div>
            <div className="mt-1 font-semibold text-zinc-900">${trade.amount}</div>
          </div>
          <div className="rounded-2xl bg-zinc-50 p-3">
            <div className="text-xs text-zinc-500">期限</div>
            <div className="mt-1 font-semibold text-zinc-900">{trade.term_days} 天</div>
          </div>
        </div>
      </Card>

      <RepaymentPlan
        role={role}
        schedules={schedules}
        onUpload={(period) => {
          const s = schedules.find((x) => x.period === period)
          if (!s) return
          setProofTitle(`上传第 ${period} 期还款凭证`)
          setProofScheduleId(s.id)
          setProofUrl("")
          setProofAmount(s.total)
          setProofOpen(true)
        }}
        onConfirm={async (period) => {
          if (!user) return
          const s = schedules.find((x) => x.period === period)
          if (!s) return
          setSubmitting(true)
          setErr(null)
          try {
            await apiV1.post(`/trades/${trade.id}/confirm-repayment`, { schedule_id: s.id, confirmed: true })
            await refresh()
          } catch (e: unknown) {
            setErr(errorMessage(e, "确认失败"))
          } finally {
            setSubmitting(false)
          }
        }}
      />

      {err ? (
        <div className="rounded-2xl bg-red-50 p-3 text-sm text-red-700">{err}</div>
      ) : null}

      {actions.length ? (
        <div className="space-y-2">
          {actions.map((a) => (
            <Button key={a.key} className="w-full" disabled={submitting} onClick={a.onClick}>{a.label}</Button>
          ))}
        </div>
      ) : null}

      <DisputeSection
        tradeId={trade.id}
        tradeStatus={trade.status}
        disputes={disputes}
        submitting={submitting}
        setSubmitting={setSubmitting}
        onCreated={refresh}
        onError={(m) => setErr(m)}
      />

      <ProofSheet
        open={proofOpen}
        title={proofTitle || "提交"}
        defaultUrl={proofUrl}
        defaultAmount={proofAmount}
        submitting={submitting}
        onClose={() => setProofOpen(false)}
        onSubmit={async ({ url, amount, note }) => {
          if (!user) return
          setSubmitting(true)
          setErr(null)
          try {
            if (trade.status === "matched" && role === "lender") {
              await apiV1.post(`/trades/${trade.id}/confirm-lend`, { proof_url: url, amount, note })
            } else if ((trade.status === "repayment_confirmed" || trade.status === "repaying") && role === "borrower") {
              if (!proofScheduleId) throw new Error("missing schedule")
              await apiV1.post(`/trades/${trade.id}/repay`, { schedule_id: proofScheduleId, proof_url: url, amount, note })
            }
            setProofOpen(false)
            await refresh()
          } catch (e: unknown) {
            setErr(errorMessage(e, "提交失败"))
          } finally {
            setSubmitting(false)
          }
        }}
      />

    </div>
  )
}
