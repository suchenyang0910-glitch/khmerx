import { useEffect, useMemo, useState } from "react"
import { Link } from "react-router-dom"
import Card from "@/components/ui/Card"
import Segmented from "@/components/ui/Segmented"
import { useI18n } from "@/i18n"
import { fetchMyOrders } from "@/api/v1"
import type { BusinessType, UnifiedOrder } from "@/api/types"
import { errorMessage } from "@/utils/errors"

type Filter = "all" | BusinessType

function btLabel(bt: Filter, t: (k: string, vars?: Record<string, string | number>) => string) {
  if (bt === "all") return t("orders.all")
  if (bt === "loan") return t("orders.loan")
  if (bt === "rental") return t("orders.rental")
  if (bt === "installment") return t("orders.installment")
  if (bt === "pawn") return t("orders.pawn")
  return bt
}

function amount(n: number) {
  if (!Number.isFinite(n)) return "0"
  return n % 1 === 0 ? String(n.toFixed(0)) : String(n.toFixed(2))
}

function targetLink(o: UnifiedOrder) {
  if (o.source_type === "finance_application") return `/applications/${o.source_id}`
  if (o.source_type === "p2p_trade") return `/trade/${o.source_id}`
  return "/trades"
}

export default function Orders() {
  const { t } = useI18n()
  const [filter, setFilter] = useState<Filter>("all")
  const [loading, setLoading] = useState(false)
  const [err, setErr] = useState<string | null>(null)
  const [items, setItems] = useState<UnifiedOrder[]>([])

  const options = useMemo(
    () =>
      (["all", "loan", "rental", "installment", "pawn"] as const).map((v) => ({
        value: v,
        label: btLabel(v, t),
      })),
    [t],
  )

  useEffect(() => {
    let cancelled = false
    setLoading(true)
    setErr(null)
    fetchMyOrders({ business_type: filter === "all" ? undefined : filter, limit: 50, offset: 0 })
      .then((res) => {
        if (!cancelled) setItems(res)
      })
      .catch((e: unknown) => {
        if (!cancelled) setErr(errorMessage(e, t("common.requestFailed")))
      })
      .finally(() => {
        if (!cancelled) setLoading(false)
      })

    return () => {
      cancelled = true
    }
  }, [filter, t])

  return (
    <div className="space-y-4">
      <div className="text-base font-semibold text-zinc-900">{t("orders.title")}</div>
      <Segmented<Filter> value={filter} options={options} onChange={(v) => setFilter(v)} />

      {loading ? (
        <div className="space-y-3">
          <div className="h-24 animate-pulse rounded-2xl bg-white" />
          <div className="h-24 animate-pulse rounded-2xl bg-white" />
        </div>
      ) : err ? (
        <Card className="p-4">
          <div className="text-sm font-semibold text-zinc-900">{t("common.requestFailed")}</div>
          <div className="mt-2 text-sm text-zinc-600">{err}</div>
        </Card>
      ) : items.length === 0 ? (
        <Card className="p-4">
          <div className="text-sm text-zinc-700">{t("orders.empty")}</div>
          <div className="mt-2 text-xs text-zinc-500">{t("orders.emptyDesc")}</div>
          <div className="mt-3">
            <Link to="/services" className="text-sm text-blue-600">{t("orders.gotoServices")}</Link>
          </div>
        </Card>
      ) : (
        <div className="space-y-3">
          {items.map((o) => (
            <Link key={o.id} to={targetLink(o)}>
              <Card className="p-4">
                <div className="flex items-start justify-between gap-3">
                  <div>
                    <div className="text-sm font-semibold text-zinc-900">{btLabel(o.business_type, t)}</div>
                    <div className="mt-1 text-xs text-zinc-500">{t("orders.status", { status: o.status })}</div>
                    {o.due_at ? (
                      <div className="mt-1 text-xs text-zinc-500">{t("orders.dueAt", { at: o.due_at })}</div>
                    ) : null}
                  </div>
                  <div className="text-right">
                    <div className="text-sm font-bold text-zinc-900">${amount(Number(o.principal || 0))}</div>
                    {o.total_due ? (
                      <div className="mt-1 text-xs text-zinc-500">{t("orders.totalDue", { amount: amount(Number(o.total_due || 0)) })}</div>
                    ) : null}
                  </div>
                </div>
              </Card>
            </Link>
          ))}
        </div>
      )}
    </div>
  )
}
