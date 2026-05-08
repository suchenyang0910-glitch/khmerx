import { useEffect, useMemo, useState } from "react"
import { useNavigate } from "react-router-dom"
import Card from "@/components/ui/Card"
import Badge from "@/components/ui/Badge"
import Button from "@/components/ui/Button"
import Modal from "@/components/ui/Modal"
import Segmented from "@/components/ui/Segmented"
import { apiV1 } from "@/api/client"
import { useAuthStore } from "@/stores/authStore"
import { errorMessage } from "@/utils/errors"
import { Shield, TrendingUp } from "lucide-react"
import { useI18n } from "@/i18n"

type Tab = "steady" | "recommended" | "high"

type MarketOffer = {
  id: string
  borrower_id: string
  amount: number
  term_days: number
  rate_percent: number
  interest: number
  received_amount: number
  repay_amount: number
  status: string
  borrower_credit_level: "A" | "B" | "C" | "D"
  borrower_completed_trades: number
  borrower_overdue_count: number
  risk_level: "low" | "mid" | "high"
  is_new_user: boolean
  created_at?: string | null
}

export default function Lend() {
  const nav = useNavigate()
  const { t } = useI18n()
  const me = useAuthStore((s) => s.user)
  const [tab, setTab] = useState<Tab>("steady")
  const [offers, setOffers] = useState<MarketOffer[]>([])
  const [loading, setLoading] = useState(false)

  const [open, setOpen] = useState(false)
  const [selected, setSelected] = useState<MarketOffer | null>(null)
  const [confirming, setConfirming] = useState(false)
  const [err, setErr] = useState<string | null>(null)

  useEffect(() => {
    let cancelled = false
    const run = async () => {
      setLoading(true)
      setErr(null)
      try {
        const res = await apiV1.get<{ ok: boolean; data: MarketOffer[] }>("/offers", { params: { tab } })
        const list = res.data.data || []
        if (!cancelled) setOffers(list)
      } catch (e: unknown) {
        if (!cancelled) setErr(errorMessage(e, t("lend.loadFailed")))
      } finally {
        if (!cancelled) setLoading(false)
      }
    }
    run()
    return () => {
      cancelled = true
    }
  }, [tab])

  const filtered = useMemo(() => {
    const scored = offers.map((o) => {
      const riskScore = (o.risk_level === "low" ? 0 : o.risk_level === "mid" ? 40 : 80) + (o.is_new_user ? 20 : 0)
      return { offer: o, creditLevel: o.borrower_credit_level, isNew: o.is_new_user, riskScore }
    })

    if (tab === "steady") {
      return scored
        .filter((x) => (x.creditLevel === "A" || x.creditLevel === "B") && !x.isNew && x.offer.amount <= 300 && x.offer.term_days <= 14 && x.riskScore < 60)
        .sort((a, b) => a.riskScore - b.riskScore)
    }
    if (tab === "high") {
      return scored.sort((a, b) => b.offer.rate_percent - a.offer.rate_percent)
    }
    return scored
      .filter((x) => x.riskScore < 80)
      .sort((a, b) => (b.offer.rate_percent * 2 - a.riskScore) - (a.offer.rate_percent * 2 - b.riskScore))
  }, [offers, tab])

  const openConfirm = async (offer: MarketOffer) => {
    setSelected(offer)
    setErr(null)
    setOpen(true)
  }

  return (
    <div className="space-y-4">
      <div>
        <div className="text-sm font-semibold text-zinc-900">{t("lend.market")}</div>
        <div className="mt-1 text-xs text-zinc-500">{t("lend.marketDesc")}</div>
      </div>

      <Segmented<Tab>
        value={tab}
        onChange={setTab}
        options={[
          { value: "steady", label: t("lend.tabSteady") },
          { value: "recommended", label: t("lend.tabRecommended") },
          { value: "high", label: t("lend.tabHigh") },
        ]}
      />

      {loading ? (
        <div className="space-y-3">
          <div className="h-24 animate-pulse rounded-2xl bg-white" />
          <div className="h-24 animate-pulse rounded-2xl bg-white" />
        </div>
      ) : err ? (
        <Card className="p-4">
          <div className="text-sm font-semibold text-zinc-900">{t("lend.loadFailed")}</div>
          <div className="mt-2 text-sm text-zinc-600">{err}</div>
        </Card>
      ) : filtered.length === 0 ? (
        <Card className="p-4">
          <div className="text-sm text-zinc-700">{t("lend.empty")}</div>
          <div className="mt-1 text-xs text-zinc-500">{t("lend.emptyDesc")}</div>
        </Card>
      ) : (
        <div className="space-y-3">
          {filtered.map(({ offer, creditLevel, isNew }) => {
            const rb = offer.risk_level === "low" ? { label: t("lend.riskLow"), tone: "green" as const } : offer.risk_level === "mid" ? { label: t("lend.riskMid"), tone: "yellow" as const } : { label: t("lend.riskHigh"), tone: "red" as const }
            const profit = offer.interest
            return (
              <Card key={offer.id} className="p-4">
                <div className="flex items-center justify-between">
                  <div className="text-lg font-bold text-zinc-900">${offer.amount}</div>
                  <div className="text-green-600 font-bold">+${profit.toFixed(2)}</div>
                </div>
                <div className="mt-1 text-xs text-zinc-500">{offer.term_days}{t("borrow.days")} · {t("lend.yield")} {offer.rate_percent}%</div>
                <div className="mt-2 flex flex-wrap items-center gap-2">
                  <Badge tone={creditLevel === "A" ? "green" : creditLevel === "B" ? "blue" : creditLevel === "C" ? "yellow" : "red"}>{t("me.credit", { level: creditLevel })}</Badge>
                  <Badge tone={rb.tone}>{rb.label}</Badge>
                  {isNew ? <Badge tone="red">{t("lend.newUser")}</Badge> : null}
                  <Badge tone="zinc">{t("lend.completed", { count: offer.borrower_completed_trades })}</Badge>
                  <Badge tone={offer.borrower_overdue_count > 0 ? "yellow" : "zinc"}>{t("lend.overdue", { count: offer.borrower_overdue_count })}</Badge>
                </div>

                <Button className="mt-3 w-full" onClick={() => openConfirm(offer)}>{t("lend.lendConfirm")}</Button>
              </Card>
            )
          })}
        </div>
      )}

      <Card className="p-4">
        <div className="flex items-start gap-3">
          <div className="flex h-10 w-10 items-center justify-center rounded-2xl bg-zinc-100 text-zinc-700">
            <Shield className="h-5 w-5" />
          </div>
          <div>
            <div className="text-sm font-semibold text-zinc-900">{t("lend.funds")}</div>
            <div className="mt-1 text-sm text-zinc-600">{t("lend.fundsDesc")}</div>
          </div>
        </div>
      </Card>

      <Modal open={open} title={t("lend.modalTitle")} onClose={() => setOpen(false)}>
        <div className="space-y-3">
          {selected ? (
            <>
              <Card className="p-3">
                <div className="flex items-center justify-between">
                  <div className="text-sm font-semibold text-zinc-900">{t("lend.youWillLend", { amount: selected.amount })}</div>
                  <Badge tone="zinc">{selected.term_days}{t("borrow.days")}</Badge>
                </div>
                <div className="mt-2 grid grid-cols-2 gap-2">
                  <div className="rounded-2xl bg-zinc-50 p-3">
                    <div className="text-xs text-zinc-500">{t("lend.expectedProfit")}</div>
                    <div className="mt-1 text-base font-semibold text-green-700">+${selected.interest.toFixed(2)}</div>
                  </div>
                  <div className="rounded-2xl bg-zinc-50 p-3">
                    <div className="text-xs text-zinc-500">{t("lend.receiveAtDue")}</div>
                    <div className="mt-1 text-base font-semibold text-zinc-900">${selected.repay_amount.toFixed(2)}</div>
                  </div>
                </div>
              </Card>

              <div className="rounded-2xl bg-amber-50 p-3 text-sm text-amber-900">
                <div className="flex items-start gap-2">
                  <TrendingUp className="mt-0.5 h-4 w-4" />
                  <div>
                    <div className="font-semibold">{t("lend.warnTitle")}</div>
                    <div className="mt-1 text-xs">{t("lend.warnDesc")}</div>
                  </div>
                </div>
              </div>

              <Button
                className="w-full"
                disabled={!me || confirming}
                onClick={async () => {
                  if (!me) return
                  setConfirming(true)
                  setErr(null)
                  try {
                    const res = await apiV1.post<{ ok: boolean; data: { trade_id: string } }>(`/offers/${selected.id}/match`, { confirm_risk: true })
                    setOpen(false)
                    nav(`/trade/${res.data.data.trade_id}`)
                  } catch (e: unknown) {
                    setErr(errorMessage(e, t("lend.matchFailed")))
                  } finally {
                    setConfirming(false)
                  }
                }}
              >
                {confirming ? t("common.processing") : t("lend.confirmMatch")}
              </Button>
            </>
          ) : (
            <div className="text-sm text-zinc-600">{t("lend.pickOffer")}</div>
          )}

          {err ? <div className="rounded-2xl bg-red-50 p-3 text-sm text-red-700">{err}</div> : null}
        </div>
      </Modal>
    </div>
  )
}
