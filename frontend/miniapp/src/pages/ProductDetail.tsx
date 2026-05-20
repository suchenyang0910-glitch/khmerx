import { useEffect, useMemo, useState } from "react"
import { Link, useNavigate, useParams } from "react-router-dom"
import Card from "@/components/ui/Card"
import Button from "@/components/ui/Button"
import { api } from "@/api/client"
import type { Product, FinanceBizType } from "@/api/types"
import { useI18n } from "@/i18n"
import { errorMessage } from "@/utils/errors"

function normalizeBizType(v: string | undefined): FinanceBizType | null {
  if (v === "lease" || v === "installment" || v === "pledge") return v
  return null
}

function firstImage(images: string) {
  const raw = (images || "").trim()
  if (!raw) return ""
  const parts = raw
    .split(/[,\n]/g)
    .map((s) => s.trim())
    .filter(Boolean)
  return parts[0] || ""
}

export default function ProductDetail() {
  const { t } = useI18n()
  const nav = useNavigate()
  const { bizType: rawBizType, productId } = useParams()
  const bizType = normalizeBizType(rawBizType)

  const [loading, setLoading] = useState(false)
  const [err, setErr] = useState<string | null>(null)
  const [p, setP] = useState<Product | null>(null)

  const title = useMemo(() => {
    if (bizType === "lease") return t("services.lease.title")
    if (bizType === "installment") return t("services.installment.title")
    return t("services.title")
  }, [bizType, t])

  useEffect(() => {
    if (!productId) return
    setLoading(true)
    setErr(null)
    api
      .get<Product>(`/products/${productId}`)
      .then((res) => {
        setP(res.data)
      })
      .catch((e) => {
        setErr(errorMessage(e, t("common.requestFailed")))
      })
      .finally(() => setLoading(false))
  }, [productId, t])

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
        <Link to={`/catalog/${bizType}`} className="text-sm text-blue-600">{t("catalog.back")}</Link>
      </div>

      {loading ? (
        <div className="h-40 animate-pulse rounded-2xl bg-white" />
      ) : err ? (
        <Card className="p-4">
          <div className="text-sm font-semibold text-zinc-900">{t("common.requestFailed")}</div>
          <div className="mt-2 text-sm text-zinc-600">{err}</div>
        </Card>
      ) : !p ? (
        <Card className="p-4">
          <div className="text-sm text-zinc-700">{t("catalog.notFound")}</div>
        </Card>
      ) : (
        <>
          {firstImage(p.images) ? (
            <div className="overflow-hidden rounded-2xl bg-white">
              <img src={firstImage(p.images)} alt={p.title} className="h-56 w-full object-cover" />
            </div>
          ) : null}

          <Card className="p-4">
            <div className="text-lg font-bold text-zinc-900">{p.title}</div>
            <div className="mt-2 text-sm text-zinc-600">{p.description || ""}</div>
            <div className="mt-3 flex items-center justify-between">
              <div className="text-xs text-zinc-500">{t("catalog.price")}</div>
              <div className="text-base font-bold text-zinc-900">${Number(p.price).toFixed(0)}</div>
            </div>
          </Card>

          <Button
            className="w-full"
            onClick={() => {
              const qp = new URLSearchParams({ product_id: p.id }).toString()
              nav(`/apply/${bizType}?${qp}`)
            }}
          >
            {t("catalog.apply")}
          </Button>
        </>
      )}
    </div>
  )
}

