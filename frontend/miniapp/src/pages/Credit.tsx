import { useEffect, useState } from "react"
import Card from "@/components/ui/Card"
import { useI18n } from "@/i18n"
import { fetchMyCredit } from "@/api/v1"
import type { CreditDetail } from "@/api/types"
import { errorMessage } from "@/utils/errors"

export default function Credit() {
  const { t } = useI18n()
  const [loading, setLoading] = useState(false)
  const [err, setErr] = useState<string | null>(null)
  const [data, setData] = useState<CreditDetail | null>(null)

  useEffect(() => {
    let cancelled = false
    setLoading(true)
    setErr(null)
    fetchMyCredit()
      .then((res) => {
        if (!cancelled) setData(res)
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
  }, [t])

  return (
    <div className="space-y-4">
      <div className="text-base font-semibold text-zinc-900">{t("credit.title")}</div>

      {loading ? (
        <div className="space-y-3">
          <div className="h-32 animate-pulse rounded-2xl bg-white" />
          <div className="h-40 animate-pulse rounded-2xl bg-white" />
        </div>
      ) : err ? (
        <Card className="p-4">
          <div className="text-sm font-semibold text-zinc-900">{t("common.requestFailed")}</div>
          <div className="mt-2 text-sm text-zinc-600">{err}</div>
        </Card>
      ) : !data ? (
        <Card className="p-4">
          <div className="text-sm text-zinc-700">{t("credit.empty")}</div>
        </Card>
      ) : (
        <>
          <Card className="p-4">
            <div className="grid grid-cols-2 gap-3">
              <div>
                <div className="text-xs text-zinc-500">{t("credit.score")}</div>
                <div className="mt-1 text-lg font-bold text-zinc-900">{data.credit_score}</div>
              </div>
              <div>
                <div className="text-xs text-zinc-500">{t("credit.level")}</div>
                <div className="mt-1 text-lg font-bold text-zinc-900">{data.credit_level}</div>
              </div>
              <div>
                <div className="text-xs text-zinc-500">{t("credit.limit")}</div>
                <div className="mt-1 text-lg font-bold text-zinc-900">${Number(data.max_borrow_amount || 0).toFixed(0)}</div>
              </div>
              <div>
                <div className="text-xs text-zinc-500">{t("credit.risk")}</div>
                <div className="mt-1 text-sm font-semibold text-zinc-900">{data.risk_level}</div>
              </div>
            </div>
          </Card>

          <Card className="p-4">
            <div className="text-sm font-semibold text-zinc-900">{t("credit.why")}</div>
            <div className="mt-2 space-y-2">
              {(data.reasons || []).slice(0, 3).map((r, idx) => (
                <div key={idx} className="text-sm text-zinc-700">
                  {r}
                </div>
              ))}
            </div>
          </Card>

          <Card className="p-4">
            <div className="text-sm font-semibold text-zinc-900">{t("credit.logs")}</div>
            {(data.logs || []).length === 0 ? (
              <div className="mt-2 text-sm text-zinc-600">{t("credit.noLogs")}</div>
            ) : (
              <div className="mt-2 space-y-3">
                {data.logs.slice(0, 10).map((l, idx) => (
                  <div key={idx} className="rounded-2xl bg-zinc-50 p-3">
                    <div className="flex items-start justify-between gap-3">
                      <div className="text-sm font-semibold text-zinc-900">{l.event_type}</div>
                      <div className="text-xs text-zinc-500">{l.created_at || ""}</div>
                    </div>
                    <div className="mt-1 text-sm text-zinc-700">{l.reason}</div>
                  </div>
                ))}
              </div>
            )}
          </Card>
        </>
      )}
    </div>
  )
}

