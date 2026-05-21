import { useEffect, useMemo, useState } from "react"
import { Link, useNavigate, useParams } from "react-router-dom"
import Card from "@/components/ui/Card"
import Input from "@/components/ui/Input"
import Button from "@/components/ui/Button"
import { api } from "@/api/client"
import type { Product, FinanceBizType } from "@/api/types"
import { useI18n } from "@/i18n"
import { errorMessage } from "@/utils/errors"
import { useTmaBackButton } from "@/hooks/useTmaBackButton"

function normalizeBizType(v: string | undefined): FinanceBizType | null {
  if (v === "lease" || v === "installment" || v === "pledge") return v
  return null
}

export default function Catalog() {
  const { t } = useI18n()
  const nav = useNavigate()
  const { bizType: rawBizType } = useParams()
  const bizType = normalizeBizType(rawBizType)

  useTmaBackButton(true, () => nav(-1))
  const [loading, setLoading] = useState(false)
  const [err, setErr] = useState<string | null>(null)
  const [q, setQ] = useState("")
  const [items, setItems] = useState<Product[]>([])

  const title = useMemo(() => {
    if (bizType === "lease") return t("services.lease.title")
    if (bizType === "installment") return t("services.installment.title")
    if (bizType === "pledge") return t("services.pledge.title")
    return t("services.title")
  }, [bizType, t])

  useEffect(() => {
    if (bizType !== "lease" && bizType !== "installment") return
    let cancelled = false
    setLoading(true)
    setErr(null)
    api
      .get<Product[]>("/products", {
        params: {
          source: "stock",
          category: bizType,
          search: q.trim() || undefined,
          limit: 50,
          offset: 0,
        },
      })
      .then((res) => {
        const list = (res.data || []).filter((p) => Boolean(p.is_verified))
        if (!cancelled) setItems(list)
      })
      .catch((e) => {
        if (!cancelled) setErr(errorMessage(e, t("common.requestFailed")))
      })
      .finally(() => {
        if (!cancelled) setLoading(false)
      })

    return () => {
      cancelled = true
    }
  }, [bizType, q, t])

  if (bizType !== "lease" && bizType !== "installment") {
    return (
      <Card className="p-4">
        <div className="text-sm text-zinc-700">{t("common.invalid")}</div>
        <div className="mt-3">
          <Link to="/services"><Button className="w-full">{t("services.title")}</Button></Link>
        </div>
      </Card>
    )
  }

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <div className="text-base font-semibold text-zinc-900">{title}</div>
        <Link to="/services" className="text-sm text-blue-600">{t("services.title")}</Link>
      </div>

      <Card className="p-3">
        <Input value={q} onChange={(e) => setQ(e.target.value)} placeholder={t("catalog.search")} />
      </Card>

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
          <div className="text-sm text-zinc-700">{t("catalog.empty")}</div>
          <div className="mt-1 text-xs text-zinc-500">{t("catalog.emptyDesc")}</div>
        </Card>
      ) : (
        <div className="space-y-3">
          {items.map((p) => (
            <Link key={p.id} to={`/catalog/${bizType}/${p.id}`}>
              <Card className="p-4">
                <div className="flex items-start justify-between gap-3">
                  <div>
                    <div className="text-sm font-semibold text-zinc-900">{p.title}</div>
                    <div className="mt-1 line-clamp-2 text-sm text-zinc-600">{p.description || ""}</div>
                  </div>
                  <div className="text-right">
                    <div className="text-sm font-bold text-zinc-900">${Number(p.price).toFixed(0)}</div>
                    <div className="mt-1 text-xs text-zinc-500">{t("catalog.stock")}</div>
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
