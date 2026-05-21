import { useEffect, useMemo, useState } from "react"
import { Link, useLocation, useNavigate, useParams } from "react-router-dom"
import Card from "@/components/ui/Card"
import Button from "@/components/ui/Button"
import Input from "@/components/ui/Input"
import { useAuthStore } from "@/stores/authStore"
import { useI18n } from "@/i18n"
import { createFinanceApplication } from "@/api/v1"
import { errorMessage } from "@/utils/errors"
import { api } from "@/api/client"
import type { FinanceBizType, Product } from "@/api/types"
import { useTmaBackButton } from "@/hooks/useTmaBackButton"

function normalizeBizType(v: string | undefined): FinanceBizType | null {
  if (v === "lease" || v === "installment" || v === "pledge") return v
  return null
}

export default function FinanceApply() {
  const { t } = useI18n()
  const nav = useNavigate()
  const { search } = useLocation()
  const { bizType: rawBizType } = useParams()
  const bizType = normalizeBizType(rawBizType)

  useTmaBackButton(true, () => nav(-1))

  const productId = useMemo(() => {
    const sp = new URLSearchParams(search)
    const v = (sp.get("product_id") || "").trim()
    return v || null
  }, [search])

  const user = useAuthStore((s) => s.user)

  const [fullName, setFullName] = useState(user?.name || "")
  const [city, setCity] = useState("")
  const [deviceModel, setDeviceModel] = useState("")
  const [imei, setImei] = useState("")
  const [condition, setCondition] = useState("good")
  const [locked, setLocked] = useState("no")
  const [amount, setAmount] = useState("")
  const [termMonths, setTermMonths] = useState("12")
  const [termDays, setTermDays] = useState("14")
  const [downPayment, setDownPayment] = useState("")
  const [notes, setNotes] = useState("")
  const [submitting, setSubmitting] = useState(false)
  const [err, setErr] = useState<string | null>(null)

  const [product, setProduct] = useState<Product | null>(null)
  const [loadingProduct, setLoadingProduct] = useState(false)

  useEffect(() => {
    if (bizType === "lease" || bizType === "installment") {
      if (product && Number(product.price) > 0) {
        setAmount(String(Number(product.price)))
      }
    }
  }, [bizType, product])

  useEffect(() => {
    if (!productId) {
      setProduct(null)
      return
    }
    if (bizType !== "lease" && bizType !== "installment") return
    let cancelled = false
    setLoadingProduct(true)
    api
      .get<Product>(`/products/${productId}`)
      .then((res) => {
        if (!cancelled) setProduct(res.data)
      })
      .catch(() => {
        if (!cancelled) setProduct(null)
      })
      .finally(() => {
        if (!cancelled) setLoadingProduct(false)
      })
    return () => {
      cancelled = true
    }
  }, [bizType, productId])

  const bizLabel = useMemo(() => {
    if (bizType === "lease") return t("services.lease.title")
    if (bizType === "installment") return t("services.installment.title")
    if (bizType === "pledge") return t("services.pledge.title")
    return ""
  }, [bizType, t])

  if (!bizType) {
    return (
      <Card className="p-4">
        <div className="text-sm text-zinc-700">{t("common.invalid")}</div>
        <div className="mt-3">
          <Link to="/services"><Button className="w-full">{t("services.title")}</Button></Link>
        </div>
      </Card>
    )
  }

  const phone = (user?.phone || "").trim()
  const phoneVerified = Boolean(user?.phone_verified)
  const abaOk = Boolean((user?.aba_account || "").trim()) && Boolean((user?.aba_name || "").trim())
  const canSubmitProfile = phoneVerified && abaOk

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <div className="text-base font-semibold text-zinc-900">{t("apply.title", { biz: bizLabel })}</div>
        <Link to="/applications" className="text-sm text-blue-600">{t("services.my")}</Link>
      </div>

      {!canSubmitProfile ? (
        <Card className="p-4">
          <div className="text-sm font-semibold text-zinc-900">{t("apply.needProfile")}</div>
          <div className="mt-2 text-sm text-zinc-600">{t("setup.desc")}</div>
          <div className="mt-3">
            <Link to={`/setup?next=${encodeURIComponent(`/apply/${bizType}`)}&require=phone`}>
              <Button className="w-full">{t("apply.gotoSetup")}</Button>
            </Link>
          </div>
        </Card>
      ) : null}

      {(bizType === "lease" || bizType === "installment") && !productId ? (
        <Card className="p-4">
          <div className="text-sm font-semibold text-zinc-900">{t("apply.needPickProduct")}</div>
          <div className="mt-2 text-sm text-zinc-600">{t("apply.pickProductDesc")}</div>
          <div className="mt-3">
            <Link to={`/catalog/${bizType}`}>
              <Button className="w-full">{t("services.choose")}</Button>
            </Link>
          </div>
        </Card>
      ) : null}

      {(bizType === "lease" || bizType === "installment") && productId ? (
        <Card className="p-4">
          <div className="text-sm font-semibold text-zinc-900">{t("apply.product")}</div>
          {loadingProduct ? (
            <div className="mt-2 h-10 animate-pulse rounded-2xl bg-zinc-50" />
          ) : product ? (
            <div className="mt-2 flex items-start justify-between gap-3">
              <div>
                <div className="text-sm font-semibold text-zinc-900">{product.title}</div>
                <div className="mt-1 text-xs text-zinc-500">{t("apply.productId", { id: product.id })}</div>
              </div>
              <div className="text-sm font-bold text-zinc-900">${Number(product.price).toFixed(0)}</div>
            </div>
          ) : (
            <div className="mt-2 text-sm text-amber-700">{t("apply.productLoadFailed")}</div>
          )}
        </Card>
      ) : null}

      <Card className="p-4">
        <div className="grid gap-3">
          <div>
            <div className="text-xs text-zinc-500">{t("apply.field.fullName")}</div>
            <Input value={fullName} onChange={(e) => setFullName(e.target.value)} placeholder={t("apply.field.fullName")} />
          </div>
          <div>
            <div className="text-xs text-zinc-500">{t("apply.field.phone")}</div>
            <Input value={phone} readOnly />
          </div>
          <div>
            <div className="text-xs text-zinc-500">{t("apply.field.city")}</div>
            <Input value={city} onChange={(e) => setCity(e.target.value)} placeholder={t("apply.field.city")} />
          </div>

          {bizType === "pledge" ? (
            <div>
              <div className="text-xs text-zinc-500">{t("apply.field.deviceModel")}</div>
              <Input value={deviceModel} onChange={(e) => setDeviceModel(e.target.value)} placeholder={t("apply.field.deviceModel")} />
            </div>
          ) : null}

          {bizType === "installment" ? (
            <div>
              <div className="text-xs text-zinc-500">{t("apply.field.downPayment")}</div>
              <Input value={downPayment} onChange={(e) => setDownPayment(e.target.value)} placeholder="USD" inputMode="decimal" />
            </div>
          ) : null}

          {bizType === "pledge" ? (
            <>
              <div>
                <div className="text-xs text-zinc-500">{t("apply.field.imei")}</div>
                <Input value={imei} onChange={(e) => setImei(e.target.value)} placeholder={t("apply.field.imei")} />
              </div>
              <div className="grid grid-cols-2 gap-3">
                <div>
                  <div className="text-xs text-zinc-500">{t("apply.field.condition")}</div>
                  <select
                    value={condition}
                    onChange={(e) => setCondition(e.target.value)}
                    className="mt-1 w-full rounded-2xl border border-zinc-200 bg-white px-3 py-2 text-sm text-zinc-900"
                  >
                    <option value="good">{t("apply.condition.good")}</option>
                    <option value="fair">{t("apply.condition.fair")}</option>
                    <option value="poor">{t("apply.condition.poor")}</option>
                  </select>
                </div>
                <div>
                  <div className="text-xs text-zinc-500">{t("apply.field.locked")}</div>
                  <select
                    value={locked}
                    onChange={(e) => setLocked(e.target.value)}
                    className="mt-1 w-full rounded-2xl border border-zinc-200 bg-white px-3 py-2 text-sm text-zinc-900"
                  >
                    <option value="no">{t("apply.lock.no")}</option>
                    <option value="yes">{t("apply.lock.yes")}</option>
                  </select>
                </div>
              </div>
            </>
          ) : null}

          <div className="grid grid-cols-2 gap-3">
            <div>
              <div className="text-xs text-zinc-500">{t("apply.field.amount")}</div>
              <Input
                value={amount}
                onChange={(e) => setAmount(e.target.value)}
                placeholder="USD"
                inputMode="decimal"
                readOnly={(bizType === "lease" || bizType === "installment") && Boolean(product)}
              />
            </div>
            <div>
              <div className="text-xs text-zinc-500">
                {bizType === "pledge" ? t("apply.field.termDays") : t("apply.field.termMonths")}
              </div>
              {bizType === "pledge" ? (
                <select
                  value={termDays}
                  onChange={(e) => setTermDays(e.target.value)}
                  className="mt-1 w-full rounded-2xl border border-zinc-200 bg-white px-3 py-2 text-sm text-zinc-900"
                >
                  <option value="7">7</option>
                  <option value="14">14</option>
                  <option value="30">30</option>
                </select>
              ) : (
                <select
                  value={termMonths}
                  onChange={(e) => setTermMonths(e.target.value)}
                  className="mt-1 w-full rounded-2xl border border-zinc-200 bg-white px-3 py-2 text-sm text-zinc-900"
                >
                  <option value="3">3</option>
                  <option value="6">6</option>
                  <option value="12">12</option>
                  <option value="18">18</option>
                  <option value="24">24</option>
                </select>
              )}
            </div>
          </div>

          <div>
            <div className="text-xs text-zinc-500">{t("apply.field.notes")}</div>
            <textarea
              value={notes}
              onChange={(e) => setNotes(e.target.value)}
              rows={4}
              className="mt-1 w-full rounded-2xl border border-zinc-200 bg-white px-3 py-2 text-sm text-zinc-900"
            />
          </div>
        </div>
      </Card>

      {err ? <div className="rounded-2xl bg-red-50 p-3 text-sm text-red-700">{err}</div> : null}

      <Button
        className="w-full"
        disabled={submitting || !canSubmitProfile}
        onClick={async () => {
          setErr(null)
          if (!canSubmitProfile) {
            setErr(t("apply.needProfile"))
            return
          }
          if ((bizType === "lease" || bizType === "installment") && !productId) {
            setErr(t("apply.needPickProduct"))
            return
          }
          setSubmitting(true)
          try {
            const payload = {
              full_name: fullName.trim(),
              phone,
              city: city.trim(),
              product_id: (bizType === "lease" || bizType === "installment") ? productId : null,
              product_title: (bizType === "lease" || bizType === "installment") ? (product?.title || null) : null,
              device_model: bizType === "pledge" ? deviceModel.trim() : null,
              amount: (bizType === "lease" || bizType === "installment") ? String(Number(product?.price || 0) || "") : amount.trim(),
              term_months: bizType === "pledge" ? null : termMonths,
              term_days: bizType === "pledge" ? termDays : null,
              down_payment: bizType === "installment" ? downPayment.trim() : null,
              imei: bizType === "pledge" ? imei.trim() : null,
              condition: bizType === "pledge" ? condition : null,
              locked: bizType === "pledge" ? locked : null,
              notes: notes.trim(),
            }
            const created = await createFinanceApplication({ biz_type: bizType, payload })
            nav(`/applications/${created.id}`)
          } catch (e: unknown) {
            setErr(errorMessage(e, t("common.requestFailed")))
          } finally {
            setSubmitting(false)
          }
        }}
      >
        {submitting ? t("apply.submitting") : t("apply.submit")}
      </Button>
    </div>
  )
}
