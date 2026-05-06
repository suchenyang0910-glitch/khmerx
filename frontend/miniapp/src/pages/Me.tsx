import { Link } from "react-router-dom"
import { useEffect, useState } from "react"
import Card from "@/components/ui/Card"
import Badge from "@/components/ui/Badge"
import Button from "@/components/ui/Button"
import { useAuthStore } from "@/stores/authStore"
import { scoreToLevel } from "@/utils/credit"
import { Bell } from "lucide-react"
import { fetchNotificationSettings, updateNotificationSettings, type NotificationSettings } from "@/api/v1"

export default function Me() {
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
  if (risk?.overdue_count) reasons.push(`有 ${risk.overdue_count} 次逾期记录`)
  if (risk?.default_count) reasons.push(`有 ${risk.default_count} 次违约记录`)
  if (risk?.cancel_count && risk.cancel_count >= 3) reasons.push("取消次数偏高")
  if (risk?.block_reason) reasons.push(risk.block_reason)
  if (!reasons.length) reasons.push("暂无明显负面记录")

  return (
    <div className="space-y-4">
      <Card className="p-4">
        <div className="flex items-center justify-between">
          <div>
            <div className="text-sm font-semibold text-zinc-900">{user?.name || ""}</div>
            <div className="mt-1 text-xs text-zinc-500">tg_id: {user?.tg_id}</div>
          </div>
          <Badge tone={level === "A" ? "green" : level === "B" ? "blue" : level === "C" ? "yellow" : "red"}>信用 {level}</Badge>
        </div>
        <div className="mt-3 grid grid-cols-2 gap-2">
          <div className="rounded-2xl bg-zinc-50 p-3">
            <div className="text-xs text-zinc-500">手机号</div>
            <div className="mt-1 text-sm font-medium text-zinc-900">{user?.phone || "未填写"}</div>
          </div>
          <div className="rounded-2xl bg-zinc-50 p-3">
            <div className="text-xs text-zinc-500">ABA</div>
            <div className="mt-1 text-sm font-medium text-zinc-900">{user?.aba_account ? "已绑定" : "未绑定"}</div>
          </div>
        </div>
        <div className="mt-3">
          <Link to="/setup"><Button variant="secondary" className="w-full">修改资料</Button></Link>
        </div>
      </Card>

      <Card className="p-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="flex h-9 w-9 items-center justify-center rounded-2xl bg-blue-50 text-blue-700">
              <Bell className="h-5 w-5" />
            </div>
            <div>
              <div className="text-sm font-semibold text-zinc-900">通知</div>
              <div className="mt-1 text-xs text-zinc-500">还款提醒、系统消息、争议处理结果</div>
            </div>
          </div>
          <Link to="/notifications" className="text-sm text-blue-600">查看</Link>
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
              还款提醒：{ns.repayment_reminders ? "开" : "关"}
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
              争议更新：{ns.dispute_updates ? "开" : "关"}
            </Button>
          </div>
        ) : null}
      </Card>

      <Card className="p-4">
        <div className="text-sm font-semibold text-zinc-900">风控解释（避免投诉）</div>
        <div className="mt-2 text-sm text-zinc-700">你的风控状态：<span className="font-semibold">{risk?.risk_level || user?.risk_level || "normal"}</span></div>
        <div className="mt-2 space-y-1 text-sm text-zinc-600">
          {reasons.map((r) => (
            <div key={r}>- {r}</div>
          ))}
        </div>
      </Card>

      <Card className="p-4">
        <div className="text-sm font-semibold text-zinc-900">如何提高额度</div>
        <div className="mt-2 space-y-1 text-sm text-zinc-600">
          <div>- 完成 1-2 笔借款并按时还款</div>
          <div>- 避免逾期与频繁取消</div>
          <div>- 绑定手机号与 ABA 信息</div>
        </div>
      </Card>
    </div>
  )
}
