import { useEffect, useMemo, useState } from "react"
import { Link, useParams } from "react-router-dom"
import Card from "@/components/ui/Card"
import Badge from "@/components/ui/Badge"
import Button from "@/components/ui/Button"
import { useI18n } from "@/i18n"
import { fetchApplicationDetail } from "@/api/v1"
import type { FinanceApplication } from "@/api/types"
import { errorMessage } from "@/utils/errors"

export default function ApplicationDetail() {
  const { t } = useI18n()
  const { applicationId } = useParams()
  const [item, setItem] = useState<FinanceApplication | null>(null)
  const [err, setErr] = useState<string | null>(null)

  useEffect(() => {
    if (!applicationId) return
    let mounted = true
    fetchApplicationDetail(applicationId)
      .then((v) => {
        if (mounted) setItem(v)
      })
      .catch((e) => {
        if (mounted) setErr(errorMessage(e, t("common.requestFailed")))
      })
    return () => {
      mounted = false
    }
  }, [applicationId, t])

  const bizTitle = useMemo(() => {
    if (!item) return ""
    if (item.biz_type === "lease") return t("services.lease.title")
    if (item.biz_type === "installment") return t("services.installment.title")
    if (item.biz_type === "pledge") return t("services.pledge.title")
    return item.biz_type
  }, [item, t])

  const statusText = useMemo(() => {
    if (!item) return ""
    const k = `applications.status.${item.status}`
    const v = t(k)
    return v === k ? String(item.status) : v
  }, [item, t])

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <div className="text-base font-semibold text-zinc-900">{t("applications.detailTitle")}</div>
        <Link to="/applications" className="text-sm text-blue-600">{t("applications.title")}</Link>
      </div>

      {err ? <div className="rounded-2xl bg-red-50 p-3 text-sm text-red-700">{err}</div> : null}

      {item ? (
        <Card className="p-4">
          <div className="flex items-start justify-between gap-3">
            <div>
              <div className="text-sm font-semibold text-zinc-900">{bizTitle}</div>
              <div className="mt-1 text-xs text-zinc-500">{item.created_at ? new Date(item.created_at).toLocaleString() : ""}</div>
            </div>
            <Badge tone={item.status === "approved" ? "green" : item.status === "rejected" ? "red" : "blue"}>
              {statusText}
            </Badge>
          </div>

          <div className="mt-4 grid gap-2 text-sm">
            {Object.entries(item.payload || {}).map(([k, v]) => (
              <div key={k} className="flex items-start justify-between gap-3 rounded-2xl bg-zinc-50 p-3">
                <div className="text-xs text-zinc-500">{k}</div>
                <div className="text-right text-sm text-zinc-900">{v == null ? "" : String(v)}</div>
              </div>
            ))}
          </div>

          <div className="mt-4">
            <Link to="/services">
              <Button variant="secondary" className="w-full">{t("services.title")}</Button>
            </Link>
          </div>
        </Card>
      ) : (
        <div className="rounded-2xl bg-white p-4 text-sm text-zinc-600">{t("common.processing")}</div>
      )}
    </div>
  )
}
