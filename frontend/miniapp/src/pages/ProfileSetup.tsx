import { useEffect, useMemo, useState } from "react"
import { useNavigate } from "react-router-dom"
import Card from "@/components/ui/Card"
import Input from "@/components/ui/Input"
import Button from "@/components/ui/Button"
import Badge from "@/components/ui/Badge"
import { useAuthStore } from "@/stores/authStore"
import { errorMessage } from "@/utils/errors"
import { useTelegram } from "@/hooks/useTelegram"
import { apiV1 } from "@/api/client"

export default function ProfileSetup() {
  const nav = useNavigate()
  const { tg } = useTelegram()
  const user = useAuthStore((s) => s.user)
  const requestPhoneOtp = useAuthStore((s) => s.requestPhoneOtp)
  const verifyPhoneOtp = useAuthStore((s) => s.verifyPhoneOtp)
  const updateAba = useAuthStore((s) => s.updateAba)
  const refreshMe = useAuthStore((s) => s.refreshMe)

  const [phone, setPhone] = useState(user?.phone || "")
  const [otpCode, setOtpCode] = useState("")
  const [otpSent, setOtpSent] = useState(false)
  const [otpDevCode, setOtpDevCode] = useState<string | null>(null)
  const [otpCooldown, setOtpCooldown] = useState(0)
  const [abaAccount, setAbaAccount] = useState(user?.aba_account || "")
  const [abaName, setAbaName] = useState(user?.aba_name || "")
  const [saving, setSaving] = useState(false)
  const [err, setErr] = useState<string | null>(null)

  const phoneOk = useMemo(() => phone.trim().length >= 8, [phone])
  const phoneVerified = Boolean(user?.phone_verified)
  const abaOk = useMemo(() => abaAccount.trim().length >= 6 && abaName.trim().length >= 1, [abaAccount, abaName])
  const canTelegramContact = Boolean((tg as any)?.requestContact)
  const otpCodeOk = useMemo(() => /^\d{6}$/.test(otpCode.trim()), [otpCode])

  useEffect(() => {
    if (otpCooldown <= 0) return
    const t = window.setInterval(() => setOtpCooldown((v) => Math.max(0, v - 1)), 1000)
    return () => window.clearInterval(t)
  }, [otpCooldown])

  return (
    <div className="mx-auto flex min-h-screen w-full max-w-md flex-col bg-[#F5F7FA] px-4 py-6">
      <div className="rounded-2xl bg-white p-4 shadow-sm">
        <div className="text-sm font-semibold text-zinc-900">完善资料（必须）</div>
        <div className="mt-1 text-sm text-zinc-600">手机号 + ABA 信息会用于交易确认与风控，缺失会导致流程崩。</div>
      </div>

      <Card className="mt-4 p-4">
        <div className="flex items-center justify-between">
          <div className="text-sm font-semibold text-zinc-900">手机号</div>
          <Badge tone={phoneVerified ? "green" : phoneOk ? "yellow" : "yellow"}>{phoneVerified ? "已验证" : "待验证"}</Badge>
        </div>

        {canTelegramContact ? (
          <div className="mt-3">
            <Button
              className="w-full"
              disabled={saving || phoneVerified}
              onClick={async () => {
                if (!user) return
                setSaving(true)
                setErr(null)
                try {
                  const contactRes = await new Promise<any>((resolve, reject) => {
                    ;(tg as any).requestContact((ok: boolean, info: any) => {
                      if (!ok) {
                        reject(new Error("你已取消手机号授权"))
                        return
                      }
                      if (!info || info.status !== "sent" || !info.response) {
                        reject(new Error("未获取到手机号信息"))
                        return
                      }
                      resolve(info)
                    })
                  })

                  await apiV1.post("/me/phone/verify-telegram", { response: contactRes.response })
                  await refreshMe()
                  setPhone((useAuthStore.getState().user?.phone || "").toString())
                } catch (e: unknown) {
                  setErr(errorMessage(e, "验证失败"))
                } finally {
                  setSaving(false)
                }
              }}
            >
              {phoneVerified ? "手机号已验证" : saving ? "处理中…" : "使用 Telegram 验证手机号"}
            </Button>
            <div className="mt-2 text-xs text-zinc-500">说明：会弹出 Telegram 授权弹窗，你确认后才会写入手机号。</div>
          </div>
        ) : null}

        <div className="mt-2">
          <Input value={phone} onChange={(e) => setPhone(e.target.value)} placeholder="例如：012345678" inputMode="tel" />
        </div>

        <div className="mt-3 flex gap-2">
          <Button
            className="flex-1"
            disabled={!phoneOk || saving || otpCooldown > 0}
            onClick={async () => {
              if (!user) return
              setSaving(true)
              setErr(null)
              try {
                const res = await requestPhoneOtp(phone.trim())
                setOtpSent(true)
                setOtpDevCode(res.dev_code || null)
                setOtpCooldown(60)
              } catch (e: unknown) {
                setErr(errorMessage(e, "发送验证码失败"))
              } finally {
                setSaving(false)
              }
            }}
          >
            {saving ? "处理中…" : otpCooldown > 0 ? `重新发送(${otpCooldown}s)` : "发送验证码"}
          </Button>
          <Button
            className="flex-1"
            disabled={!phoneOk || !otpSent || !otpCodeOk || saving}
            onClick={async () => {
              if (!user) return
              setSaving(true)
              setErr(null)
              try {
                await verifyPhoneOtp(phone.trim(), otpCode.trim())
              } catch (e: unknown) {
                setErr(errorMessage(e, "验证失败"))
              } finally {
                setSaving(false)
              }
            }}
          >
            {saving ? "处理中…" : "验证"}
          </Button>
        </div>

        {otpSent ? (
          <div className="mt-2 space-y-2">
            <Input value={otpCode} onChange={(e) => setOtpCode(e.target.value)} placeholder="输入 6 位验证码" inputMode="numeric" />
            {otpDevCode ? (
              <div className="text-xs text-zinc-500">本地开发验证码：{otpDevCode}</div>
            ) : null}
          </div>
        ) : null}
      </Card>

      <Card className="mt-3 p-4">
        <div className="flex items-center justify-between">
          <div className="text-sm font-semibold text-zinc-900">ABA 账户</div>
          <Badge tone={abaOk ? "green" : "yellow"}>{abaOk ? "已填写" : "待填写"}</Badge>
        </div>
        <div className="mt-2 space-y-2">
          <Input value={abaAccount} onChange={(e) => setAbaAccount(e.target.value)} placeholder="ABA 账号" />
          <Input value={abaName} onChange={(e) => setAbaName(e.target.value)} placeholder="ABA 账户名" />
        </div>
      </Card>

      {err ? (
        <div className="mt-3 rounded-2xl bg-red-50 p-3 text-sm text-red-700">{err}</div>
      ) : null}

      <div className="mt-4 space-y-2">
        <Button
          className="w-full"
          disabled={!phoneVerified || !abaOk || saving}
          onClick={async () => {
            if (!user) return
            setSaving(true)
            setErr(null)
            try {
              await updateAba(abaAccount.trim(), abaName.trim())
              nav("/", { replace: true })
            } catch (e: unknown) {
              setErr(errorMessage(e, "保存失败"))
            } finally {
              setSaving(false)
            }
          }}
        >
          {saving ? "保存中…" : phoneVerified ? "保存并继续" : "请先验证手机号"}
        </Button>
        <div className="text-xs text-zinc-500">
          说明：KhmerX 不会向陌生人主动私聊；所有通知都需要你主动触发或订阅。
        </div>
      </div>
    </div>
  )
}
