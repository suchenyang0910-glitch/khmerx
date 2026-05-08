import { useEffect, useState } from "react"
import Card from "@/components/ui/Card"
import Button from "@/components/ui/Button"
import { fetchNotifications, markNotificationRead } from "@/api/v1"
import type { Notification } from "@/api/types"
import { useI18n } from "@/i18n"

export default function Notifications() {
  const { t } = useI18n()
  const [rows, setRows] = useState<Notification[]>([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  async function reload() {
    setLoading(true)
    setError(null)
    try {
      setRows(await fetchNotifications())
    } catch {
      setError(t("noti.loadFailed"))
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    reload()
  }, [])

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <div>
          <div className="text-lg font-semibold text-zinc-900">{t("noti.title")}</div>
          <div className="mt-1 text-sm text-zinc-600">{t("noti.subtitle")}</div>
        </div>
        <Button variant="secondary" onClick={reload} disabled={loading}>
          {loading ? t("noti.refreshing") : t("noti.refresh")}
        </Button>
      </div>

      {error ? <Card className="p-4 text-sm text-red-700 bg-red-50">{error}</Card> : null}

      {rows.length === 0 ? (
        <Card className="p-4">
          <div className="text-sm text-zinc-600">{t("noti.empty")}</div>
        </Card>
      ) : (
        rows.map((n) => (
          <Card key={n.id} className="p-4">
            <div className="flex items-start justify-between gap-3">
              <div className="min-w-0">
                <div className="flex items-center gap-2">
                  <div className={`h-2 w-2 rounded-full ${n.read ? "bg-zinc-300" : "bg-blue-600"}`} />
                  <div className="text-sm font-semibold text-zinc-900 truncate">{n.title}</div>
                </div>
                <div className="mt-2 text-sm text-zinc-700 whitespace-pre-line">{n.body}</div>
                <div className="mt-2 text-xs text-zinc-500">{n.created_at ?? ""}</div>
              </div>
              {!n.read ? (
                <Button
                  variant="secondary"
                  onClick={async () => {
                    await markNotificationRead(n.id)
                    await reload()
                  }}
                >
                  {t("noti.markRead")}
                </Button>
              ) : null}
            </div>
          </Card>
        ))
      )}
    </div>
  )
}
