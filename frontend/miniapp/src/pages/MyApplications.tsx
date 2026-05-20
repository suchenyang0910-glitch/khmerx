import { useEffect, useMemo, useState } from "react"
import { Link } from "react-router-dom"
import Card from "@/components/ui/Card"
import Badge from "@/components/ui/Badge"
import Button from "@/components/ui/Button"
import { useI18n } from "@/i18n"
import { fetchMyApplications } from "@/api/v1"
import type { FinanceApplication, FinanceBizType } from "@/api/types"
import { errorMessage } from "@/utils/errors"

type TFunc = (key: string, vars?: Record<string, string | number>) => string

function bizLabel(t: TFunc, bt: string) {
  if (bt === "lease") return t("services.lease.title")
  if (bt === "installment") return t("services.installment.title")
  if (bt === "pledge") return t("services.pledge.title")
  return bt
}

function statusLabel(t: TFunc, status: string) {
  const k = `applications.status.${status}`
  const v = t(k)
  return v === k ? status : v
}

export default function MyApplications() {
  const { t } = useI18n()
  const [bizType, setBizType] = useState<FinanceBizType | "all">("all")
  const [items, setItems] = useState<FinanceApplication[]>([])
  const [loading, setLoading] = useState(false)
  const [err, setErr] = useState<string | null>(null)

  const load = async (bt: FinanceBizType | "all") => {
    setLoading(true)
    setErr(null)
    try {
      const data = await fetchMyApplications(bt === "all" ? undefined : { biz_type: bt })
      setItems(data)
    } catch (e: unknown) {
      setErr(errorMessage(e, t("common.requestFailed")))
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    load(bizType)
  }, [bizType])

  const sorted = useMemo(() => {
    return [...items].sort((a, b) => {
      const at = a.created_at ? Date.parse(a.created_at) : 0
      const bt = b.created_at ? Date.parse(b.created_at) : 0
      return bt - at
    })
  }, [items])

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <div className="text-base font-semibold text-zinc-900">{t("applications.title")}</div>
        <Link to="/services" className="text-sm text-blue-600">{t("services.title")}</Link>
      </div>

      <Card className="p-4">
        <div className="flex items-center justify-between gap-3">
          <div className="text-sm font-semibold text-zinc-900">{t("applications.filter")}</div>
          <select
            value={bizType}
            onChange={(e) => {
              const v = e.target.value
              if (v === "all" || v === "lease" || v === "installment" || v === "pledge") setBizType(v)
            }}
            className="rounded-2xl border border-zinc-200 bg-white px-3 py-2 text-sm text-zinc-900"
          >
            <option value="all">{t("applications.all")}</option>
            <option value="lease">{t("services.lease.title")}</option>
            <option value="installment">{t("services.installment.title")}</option>
            <option value="pledge">{t("services.pledge.title")}</option>
          </select>
        </div>
      </Card>

      {err ? <div className="rounded-2xl bg-red-50 p-3 text-sm text-red-700">{err}</div> : null}

      {loading ? (
        <div className="rounded-2xl bg-white p-4 text-sm text-zinc-600">{t("common.processing")}</div>
      ) : null}

      {!loading && !sorted.length ? (
        <Card className="p-4">
          <div className="text-sm text-zinc-600">{t("applications.empty")}</div>
          <div className="mt-3">
            <Link to="/services"><Button className="w-full">{t("services.apply")}</Button></Link>
          </div>
        </Card>
      ) : null}

      <div className="grid gap-3">
        {sorted.map((a) => (
          <Card key={a.id} className="p-4">
            <div className="flex items-start justify-between gap-3">
              <div>
                <div className="text-sm font-semibold text-zinc-900">{bizLabel(t, a.biz_type)}</div>
                <div className="mt-1 text-xs text-zinc-500">{a.created_at ? new Date(a.created_at).toLocaleString() : ""}</div>
              </div>
              <Badge tone={a.status === "approved" ? "green" : a.status === "rejected" ? "red" : "blue"}>
                {statusLabel(t, a.status)}
              </Badge>
            </div>
            <div className="mt-3">
              <Link to={`/applications/${a.id}`}>
                <Button variant="secondary" className="w-full">{t("applications.view")}</Button>
              </Link>
            </div>
          </Card>
        ))}
      </div>
    </div>
  )
}
