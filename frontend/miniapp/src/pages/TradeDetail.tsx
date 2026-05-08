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
import { useI18n } from "@/i18n"

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
  const { t } = useI18n()
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
      setErr(errorMessage(e, t("trade.loadFailed")))
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
        ? { title: t("trade.tip.waitTransfer"), desc: t("trade.tip.uploadWithin24h") }
        : { title: t("trade.tip.waitLend"), desc: t("trade.tip.waitLenderTransfer") }
    }
    if (trade.status === "lend_confirmed") {
      return role === "borrower"
        ? { title: t("trade.tip.lent"), desc: t("trade.tip.confirmReceive") }
        : { title: t("trade.tip.proofUploaded"), desc: t("trade.tip.waitBorrowerConfirm") }
    }
    if (trade.status === "repayment_confirmed") {
      return role === "borrower"
        ? { title: t("trade.tip.receivedConfirmed"), desc: t("trade.tip.startRepay") }
        : { title: t("trade.tip.receivedConfirmed"), desc: t("trade.tip.waitBorrowerRepay") }
    }
    if (trade.status === "repaying") {
      if (role === "borrower") {
        const next = schedules.find((s) => s.status === "pending" || s.status === "overdue")
        return next
          ? {
              title: t("trade.tip.repayingPeriod", { period: next.period }),
              desc: t("trade.tip.uploadRepayProof", { date: next.due_at ? new Date(next.due_at).toLocaleDateString() : "-" }),
            }
          : { title: t("trade.tip.repaying"), desc: t("trade.tip.waitLenderConfirm") }
      }
      const pendingConfirm = schedules.find((s) => s.status === "paid_pending")
      return pendingConfirm
        ? { title: t("trade.tip.pendingConfirm"), desc: t("trade.tip.confirmPeriod", { period: pendingConfirm.period }) }
        : { title: t("trade.tip.repaying"), desc: t("trade.tip.waitBorrowerAction") }
    }
    if (trade.status === "completed") return { title: t("trade.tip.completed"), desc: t("trade.tip.completedDesc") }
    if (trade.status === "dispute") return { title: t("trade.tip.dispute"), desc: t("trade.tip.disputeDesc") }
    return { title: t("trade.tip.status", { status: trade.status }), desc: t("trade.tip.seeDetail") }
  }, [role, schedules, trade])

  const actions = useMemo(() => {
    if (!trade || !user) return [] as Array<{ key: string; label: string; onClick: () => void }>

    if (trade.status === "matched" && role === "lender") {
      return [{
        key: "lend",
        label: t("trade.action.uploadLendProof"),
        onClick: () => {
          setProofTitle(t("trade.action.uploadLendProof"))
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
        label: t("trade.action.confirmReceive"),
        onClick: async () => {
          setSubmitting(true)
          setErr(null)
          try {
            await apiV1.post(`/trades/${trade.id}/confirm-receive`, { confirmed: true })
            await refresh()
          } catch (e: unknown) {
            setErr(errorMessage(e, t("trade.confirmFailed")))
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
          label: t("trade.action.uploadRepayProof", { period: next.period }),
          onClick: () => {
            setProofTitle(t("trade.action.uploadRepayProof", { period: next.period }))
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
        return [{ key: "confirm", label: t("trade.action.confirmRepay", { period: pending.period }), onClick: async () => {
          setSubmitting(true)
          setErr(null)
          try {
            await apiV1.post(`/trades/${trade.id}/confirm-repayment`, { schedule_id: pending.id, confirmed: true })
            await refresh()
          } catch (e: unknown) {
            setErr(errorMessage(e, t("trade.confirmFailed")))
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
        <div className="text-sm font-semibold text-zinc-900">{t("trade.unableLoad")}</div>
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
          <ArrowLeft className="h-4 w-4" /> {t("common.back")}
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
          <div className="text-sm font-semibold text-zinc-900">{t("trade.info")}</div>
          <div className="text-xs text-zinc-500">{role === "lender" ? t("trade.roleLender") : t("trade.roleBorrower")}</div>
        </div>
        <div className="mt-2 grid grid-cols-2 gap-2 text-sm">
          <div className="rounded-2xl bg-zinc-50 p-3">
            <div className="text-xs text-zinc-500">{t("trade.amount")}</div>
            <div className="mt-1 font-semibold text-zinc-900">${trade.amount}</div>
          </div>
          <div className="rounded-2xl bg-zinc-50 p-3">
            <div className="text-xs text-zinc-500">{t("trade.term")}</div>
            <div className="mt-1 font-semibold text-zinc-900">{trade.term_days}{t("borrow.days")}</div>
          </div>
        </div>
      </Card>

      <RepaymentPlan
        role={role}
        schedules={schedules}
        onUpload={(period) => {
          const s = schedules.find((x) => x.period === period)
          if (!s) return
          setProofTitle(t("trade.action.uploadRepayProof", { period }))
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
            setErr(errorMessage(e, t("trade.confirmFailed")))
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
        title={proofTitle || t("proof.confirm")}
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
            setErr(errorMessage(e, t("trade.submitFailed")))
          } finally {
            setSubmitting(false)
          }
        }}
      />

    </div>
  )
}
