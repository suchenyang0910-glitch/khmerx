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
        if (!cancelled) setErr(errorMessage(e, "加载失败"))
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
        <div className="text-sm font-semibold text-zinc-900">出借市场</div>
        <div className="mt-1 text-xs text-zinc-500">看得懂风险 · 确认收益 · 再出借</div>
      </div>

      <Segmented<Tab>
        value={tab}
        onChange={setTab}
        options={[
          { value: "steady", label: "稳健" },
          { value: "recommended", label: "推荐" },
          { value: "high", label: "高收益" },
        ]}
      />

      {loading ? (
        <div className="space-y-3">
          <div className="h-24 animate-pulse rounded-2xl bg-white" />
          <div className="h-24 animate-pulse rounded-2xl bg-white" />
        </div>
      ) : err ? (
        <Card className="p-4">
          <div className="text-sm font-semibold text-zinc-900">加载失败</div>
          <div className="mt-2 text-sm text-zinc-600">{err}</div>
        </Card>
      ) : filtered.length === 0 ? (
        <Card className="p-4">
          <div className="text-sm text-zinc-700">暂无符合条件的挂单</div>
          <div className="mt-1 text-xs text-zinc-500">你可以切换分类或稍后再来。</div>
        </Card>
      ) : (
        <div className="space-y-3">
          {filtered.map(({ offer, creditLevel, isNew }) => {
            const rb = offer.risk_level === "low" ? { label: "低风险", tone: "green" as const } : offer.risk_level === "mid" ? { label: "中风险", tone: "yellow" as const } : { label: "高风险", tone: "red" as const }
            const profit = offer.interest
            return (
              <Card key={offer.id} className="p-4">
                <div className="flex items-center justify-between">
                  <div className="text-lg font-bold text-zinc-900">${offer.amount}</div>
                  <div className="text-green-600 font-bold">+${profit.toFixed(2)}</div>
                </div>
                <div className="mt-1 text-xs text-zinc-500">{offer.term_days}天 · 收益 {offer.rate_percent}%</div>
                <div className="mt-2 flex flex-wrap items-center gap-2">
                  <Badge tone={creditLevel === "A" ? "green" : creditLevel === "B" ? "blue" : creditLevel === "C" ? "yellow" : "red"}>信用 {creditLevel}</Badge>
                  <Badge tone={rb.tone}>{rb.label}</Badge>
                  {isNew ? <Badge tone="red">新用户</Badge> : null}
                  <Badge tone="zinc">完成单 {offer.borrower_completed_trades}</Badge>
                  <Badge tone={offer.borrower_overdue_count > 0 ? "yellow" : "zinc"}>逾期 {offer.borrower_overdue_count}</Badge>
                </div>

                <Button className="mt-3 w-full" onClick={() => openConfirm(offer)}>出借（先确认）</Button>
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
            <div className="text-sm font-semibold text-zinc-900">资金说明</div>
            <div className="mt-1 text-sm text-zinc-600">平台提供撮合与风控信息，不承诺兜底。请在确认风险后出借。</div>
          </div>
        </div>
      </Card>

      <Modal open={open} title="确认出借" onClose={() => setOpen(false)}>
        <div className="space-y-3">
          {selected ? (
            <>
              <Card className="p-3">
                <div className="flex items-center justify-between">
                  <div className="text-sm font-semibold text-zinc-900">你将借出：${selected.amount}</div>
                  <Badge tone="zinc">{selected.term_days}天</Badge>
                </div>
                <div className="mt-2 grid grid-cols-2 gap-2">
                  <div className="rounded-2xl bg-zinc-50 p-3">
                    <div className="text-xs text-zinc-500">预计收益</div>
                    <div className="mt-1 text-base font-semibold text-green-700">+${selected.interest.toFixed(2)}</div>
                  </div>
                  <div className="rounded-2xl bg-zinc-50 p-3">
                    <div className="text-xs text-zinc-500">到期收回</div>
                    <div className="mt-1 text-base font-semibold text-zinc-900">${selected.repay_amount.toFixed(2)}</div>
                  </div>
                </div>
              </Card>

              <div className="rounded-2xl bg-amber-50 p-3 text-sm text-amber-900">
                <div className="flex items-start gap-2">
                  <TrendingUp className="mt-0.5 h-4 w-4" />
                  <div>
                    <div className="font-semibold">请仅在确认风险后出借</div>
                    <div className="mt-1 text-xs">下一步：接单后在交易页查看 ABA 信息并上传打款凭证。</div>
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
                    setErr(errorMessage(e, "接单失败"))
                  } finally {
                    setConfirming(false)
                  }
                }}
              >
                {confirming ? "处理中…" : "确认出借（接单）"}
              </Button>
            </>
          ) : (
            <div className="text-sm text-zinc-600">请选择一个挂单</div>
          )}

          {err ? <div className="rounded-2xl bg-red-50 p-3 text-sm text-red-700">{err}</div> : null}
        </div>
      </Modal>
    </div>
  )
}
