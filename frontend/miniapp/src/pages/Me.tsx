import { Link } from "react-router-dom"
import { useEffect, useState } from "react"
import Card from "@/components/ui/Card"
import Badge from "@/components/ui/Badge"
import Button from "@/components/ui/Button"
import { useAuthStore } from "@/stores/authStore"
import { scoreToLevel } from "@/utils/credit"
import { Bell } from "lucide-react"
import { fetchNotificationSettings, updateNotificationSettings, type NotificationSettings } from "@/api/v1"
import { SUPPORTED_LANGS, useI18n } from "@/i18n"

export default function Me() {
  const { lang, setLang, t } = useI18n()
  const user = useAuthStore((s) => s.user)
  const risk = useAuthStore((s) => s.risk)
  const level = scoreToLevel(user?.credit_score || 650)

  const [ns, setNs] = useState<NotificationSettings | null>(null)
  const [savingNs, setSavingNs] = useState(false)

  useEffect(() => {
    let mounted = true
    fetchNotificationSettings().then((v) => {
      if (mounted) setNs(v)
    }).catch(() => {})
    return () => {
      mounted = false
    }
  }, [])

  const reasons: string[] = []
  if (risk?.overdue_count) reasons.push(t("me.riskOverdue", { count: risk.overdue_count }))
  if (risk?.default_count) reasons.push(t("me.riskDefault", { count: risk.default_count }))
  if (risk?.cancel_count && risk.cancel_count >= 3) reasons.push(t("me.riskCancelHigh"))
  if (risk?.block_reason) reasons.push(risk.block_reason)
  if (!reasons.length) reasons.push(t("me.noNeg"))

  return (
    <div className="space-y-4">
      <Card className="p-4">
        <div className="flex items-center justify-between">
          <div>
            <div className="text-sm font-semibold text-zinc-900">{user?.name || ""}</div>
            <div className="mt-1 text-xs text-zinc-500">tg_id: {user?.tg_id}</div>
          </div>
          <Badge tone={level === "A" ? "green" : level === "B" ? "blue" : level === "C" ? "yellow" : "red"}>{t("me.credit", { level })}</Badge>
        </div>
        <div className="mt-3 grid grid-cols-2 gap-2">
          <div className="rounded-2xl bg-zinc-50 p-3">
            <div className="text-xs text-zinc-500">{t("me.phone")}</div>
            <div className="mt-1 text-sm font-medium text-zinc-900">{user?.phone || t("me.notSet")}</div>
          </div>
          <div className="rounded-2xl bg-zinc-50 p-3">
            <div className="text-xs text-zinc-500">{t("me.aba")}</div>
            <div className="mt-1 text-sm font-medium text-zinc-900">{user?.aba_account ? t("me.bound") : t("me.unbound")}</div>
          </div>
        </div>
        <div className="mt-3">
          <Link to="/setup"><Button variant="secondary" className="w-full">{t("auth.profileEdit")}</Button></Link>
        </div>
      </Card>

      <Card className="p-4">
        <div className="flex items-center justify-between">
          <div className="text-sm font-semibold text-zinc-900">{t("me.language")}</div>
          <div className="text-xs text-zinc-500">{lang.toUpperCase()}</div>
        </div>
        <div className="mt-3 grid grid-cols-3 gap-2">
          {SUPPORTED_LANGS.map((l) => (
            <Button key={l} variant={lang === l ? "primary" : "secondary"} onClick={() => setLang(l)}>
              {t(`lang.${l}`)}
            </Button>
          ))}
        </div>
      </Card>

      <Card className="p-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="flex h-9 w-9 items-center justify-center rounded-2xl bg-blue-50 text-blue-700">
              <Bell className="h-5 w-5" />
            </div>
            <div>
              <div className="text-sm font-semibold text-zinc-900">{t("me.notifications")}</div>
              <div className="mt-1 text-xs text-zinc-500">{t("me.notificationsDesc")}</div>
            </div>
          </div>
          <Link to="/notifications" className="text-sm text-blue-600">{t("me.view")}</Link>
        </div>

        {ns ? (
          <div className="mt-3 grid grid-cols-2 gap-2">
            <Button
              variant={ns.repayment_reminders ? "primary" : "secondary"}
              disabled={savingNs}
              onClick={async () => {
                setSavingNs(true)
                try {
                  const v = await updateNotificationSettings({ repayment_reminders: !ns.repayment_reminders })
                  setNs(v)
                } finally {
                  setSavingNs(false)
                }
              }}
            >
              {t("me.repayRemind")}：{ns.repayment_reminders ? t("me.on") : t("me.off")}
            </Button>
            <Button
              variant={ns.dispute_updates ? "primary" : "secondary"}
              disabled={savingNs}
              onClick={async () => {
                setSavingNs(true)
                try {
                  const v = await updateNotificationSettings({ dispute_updates: !ns.dispute_updates })
                  setNs(v)
                } finally {
                  setSavingNs(false)
                }
              }}
            >
              {t("me.disputeUpdates")}：{ns.dispute_updates ? t("me.on") : t("me.off")}
            </Button>
          </div>
        ) : null}
      </Card>

      <Card className="p-4">
        <div className="text-sm font-semibold text-zinc-900">{t("me.riskExplain")}</div>
        <div className="mt-2 text-sm text-zinc-700">{t("me.riskStatus")}: <span className="font-semibold">{risk?.risk_level || user?.risk_level || "normal"}</span></div>
        <div className="mt-2 space-y-1 text-sm text-zinc-600">
          {reasons.map((r) => (
            <div key={r}>- {r}</div>
          ))}
        </div>
      </Card>

      <Card className="p-4">
        <div className="text-sm font-semibold text-zinc-900">{t("me.howIncrease")}</div>
        <div className="mt-2 space-y-1 text-sm text-zinc-600">
          <div>- {t("me.how1")}</div>
          <div>- {t("me.how2")}</div>
          <div>- {t("me.how3")}</div>
        </div>
      </Card>
    </div>
  )
}
