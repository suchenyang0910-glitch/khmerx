import { useEffect, useMemo, useRef, useState } from "react"
import { useLocation, useNavigate } from "react-router-dom"
import Card from "@/components/ui/Card"
import Input from "@/components/ui/Input"
import Button from "@/components/ui/Button"
import Badge from "@/components/ui/Badge"
import { useAuthStore } from "@/stores/authStore"
import { errorMessage } from "@/utils/errors"
import { useTelegram } from "@/hooks/useTelegram"
import axios from "axios"
import { api, apiV1 } from "@/api/client"
import { useI18n } from "@/i18n"
import { useTmaTheme } from "@/hooks/useTmaTheme"

export default function ProfileSetup() {
  useTmaTheme()
  const nav = useNavigate()
  const { search } = useLocation()
  const { tg, initData } = useTelegram()
  const { t } = useI18n()
  const user = useAuthStore((s) => s.user)
  const bootstrap = useAuthStore((s) => s.bootstrap)
  const requestPhoneOtp = useAuthStore((s) => s.requestPhoneOtp)
  const verifyPhoneOtp = useAuthStore((s) => s.verifyPhoneOtp)
  const updateAba = useAuthStore((s) => s.updateAba)
  const refreshMe = useAuthStore((s) => s.refreshMe)

  const [phone, setPhone] = useState(user?.phone || "")
  const [otpCode, setOtpCode] = useState("")
  const [otpSent, setOtpSent] = useState(false)
  const [otpDevCode, setOtpDevCode] = useState<string | null>(null)
  const [otpChallengeId, setOtpChallengeId] = useState<string | null>(null)
  const [otpPhone, setOtpPhone] = useState<string | null>(null)
  const [otpCooldown, setOtpCooldown] = useState(0)
  const [abaAccount, setAbaAccount] = useState(user?.aba_account || "")
  const [abaName, setAbaName] = useState(user?.aba_name || "")
  const [saving, setSaving] = useState(false)
  const [err, setErr] = useState<string | null>(null)

  const { nextPath, requireField } = useMemo(() => {
    const sp = new URLSearchParams(search)
    const next = (sp.get("next") || "").trim()
    const req = (sp.get("require") || "").trim()
    const safeNext = next.startsWith("/") ? next : ""
    const safeReq = req === "phone" || req === "aba" ? req : ""
    return { nextPath: safeNext, requireField: safeReq }
  }, [search])

  const phoneOk = useMemo(() => phone.trim().length >= 8, [phone])
  const phoneVerified = Boolean(user?.phone_verified)
  const abaOk = useMemo(() => abaAccount.trim().length >= 1 && abaName.trim().length >= 1, [abaAccount, abaName])

  type TgContactApi = {
    requestContact?: (cb: (ok: boolean, info: unknown) => void) => void
  }
  const canTelegramContact = Boolean((tg as unknown as TgContactApi | null)?.requestContact)
  const otpCodeOk = useMemo(() => /^\d{6}$/.test(otpCode.trim()), [otpCode])

  useEffect(() => {
    if (otpCooldown <= 0) return
    const t = window.setInterval(() => setOtpCooldown((v) => Math.max(0, v - 1)), 1000)
    return () => window.clearInterval(t)
  }, [otpCooldown])

  useEffect(() => {
    if (!otpDevCode) return
    if (otpCode.trim()) return
    setOtpCode(otpDevCode)
  }, [otpDevCode, otpCode])

  const canLocalDevLogin = import.meta.env.DEV
  const autoBootstrapTried = useRef(false)

  useEffect(() => {
    if (user) return
    if (autoBootstrapTried.current) return
    const data = (initData || localStorage.getItem("khx_tma_init_data") || "").trim()
    if (!data) return
    autoBootstrapTried.current = true
    bootstrap(data).catch(() => {})
  }, [bootstrap, initData, user])

  const generateLocalAccount = async () => {
    setSaving(true)
    setErr(null)
    try {
      const tgId = 90000000 + Math.floor(Math.random() * 1000000)
      const res = await api.get<{ ok: boolean; data: { init_data: string } }>("/auth/dev-tma", {
        params: { tg_id: tgId },
      })
      const init = res.data?.data?.init_data || ""
      if (!init) throw new Error(t("dev.backendUnreachable"))
      await bootstrap(init)
    } catch (e: unknown) {
      setErr(errorMessage(e, t("dev.localLoginFailed")))
    } finally {
      setSaving(false)
    }
  }

  if (!user) {
    return (
      <div className="mx-auto flex min-h-screen w-full max-w-md flex-col bg-[#F5F7FA] px-4 py-6">
        <div className="rounded-2xl bg-white p-4 shadow-sm">
          <div className="text-sm font-semibold text-zinc-900">{t("auth.loginFailed")}</div>
          <div className="mt-2 text-sm text-zinc-600">{t("auth.openInTelegram")}</div>
          {canLocalDevLogin ? (
            <div className="mt-4">
              <Button className="w-full" disabled={saving} onClick={generateLocalAccount}>
                {saving ? t("dev.generatingAccount") : t("dev.generateAccount")}
              </Button>
            </div>
          ) : null}
          {err ? <div className="mt-3 rounded-2xl bg-red-50 p-3 text-sm text-red-700">{err}</div> : null}
        </div>
      </div>
    )
  }

  return (
    <div data-testid="page-setup" className="mx-auto flex min-h-screen w-full max-w-md flex-col bg-[#F5F7FA] px-4 py-6">
      <div className="rounded-2xl bg-white p-4 shadow-sm">
        <div className="text-sm font-semibold text-zinc-900">{t("setup.title")}</div>
        <div className="mt-1 text-sm text-zinc-600">{t("setup.desc")}</div>
      </div>

      <Card className="mt-4 p-4">
        <div className="flex items-center justify-between">
          <div className="text-sm font-semibold text-zinc-900">{t("setup.phone")}</div>
          <Badge tone={phoneVerified ? "green" : phoneOk ? "yellow" : "yellow"}>{phoneVerified ? t("setup.phoneVerified") : t("setup.phonePending")}</Badge>
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
                  const contactRes = await new Promise<{ response: string }>((resolve, reject) => {
                    ;(tg as unknown as TgContactApi).requestContact?.((ok: boolean, info: unknown) => {
                      if (!ok) {
                        reject(new Error(t("setup.phoneAuthCanceled")))
                        return
                      }
                      const r = (info || {}) as Record<string, unknown>
                      if (r.status !== "sent" || typeof r.response !== "string" || !r.response) {
                        reject(new Error(t("setup.phoneAuthMissing")))
                        return
                      }
                      resolve({ response: r.response })
                    })
                  })

                  await apiV1.post("/me/phone/verify-telegram", { response: contactRes.response })
                  await refreshMe()
                  setPhone((useAuthStore.getState().user?.phone || "").toString())
                } catch (e: unknown) {
                  setErr(errorMessage(e, t("setup.verifyFailed")))
                } finally {
                  setSaving(false)
                }
              }}
            >
              {phoneVerified ? t("setup.phoneVerifiedBtn") : saving ? t("common.processing") : t("setup.useTelegramVerify")}
            </Button>
            <div className="mt-2 text-xs text-zinc-500">{t("setup.phoneTelegramHint")}</div>
          </div>
        ) : null}

        <div className="mt-2">
          <Input
            value={phone}
            onChange={(e) => setPhone(e.target.value)}
            placeholder={t("setup.phonePlaceholder")}
            inputMode="tel"
            disabled={otpSent && !phoneVerified}
          />
          {!phoneOk && phone.trim() ? (
            <div className="mt-2 text-xs text-amber-700">{t("setup.phoneMinLen")}</div>
          ) : null}
        </div>

        <div className="mt-3 flex gap-2">
          <Button
            className="flex-1"
            disabled={!phoneOk || saving || otpCooldown > 0}
            onClick={async () => {
              setSaving(true)
              setErr(null)
              try {
                const p = phone.trim()
                const res = await requestPhoneOtp(p)
                setOtpSent(true)
                setOtpChallengeId(res.challenge_id)
                setOtpPhone(p)
                if (res.dev_code) setOtpDevCode(res.dev_code)
                setOtpCooldown(60)
              } catch (e: unknown) {
                setErr(errorMessage(e, t("setup.sendCodeFailed")))
              } finally {
                setSaving(false)
              }
            }}
          >
            {saving ? t("common.processing") : otpCooldown > 0 ? `${t("setup.sendCode")}(${otpCooldown}s)` : t("setup.sendCode")}
          </Button>
          <Button
            className="flex-1"
            disabled={!phoneOk || !otpSent || !otpCodeOk || saving}
            onClick={async () => {
              setSaving(true)
              setErr(null)
              try {
                const p = (otpPhone || phone).trim()
                await verifyPhoneOtp(p, otpCode.trim(), otpChallengeId || undefined)
              } catch (e: unknown) {
                setErr(errorMessage(e, t("setup.verifyFailed")))
              } finally {
                setSaving(false)
              }
            }}
          >
            {saving ? t("common.processing") : t("setup.verify")}
          </Button>
        </div>

        {otpSent ? (
          <div className="mt-2 space-y-2">
            <Input value={otpCode} onChange={(e) => setOtpCode(e.target.value)} placeholder={t("setup.codePlaceholder")} inputMode="numeric" />
            {otpDevCode ? (
              <div className="text-xs text-zinc-500">{t("setup.devCode", { code: otpDevCode })}</div>
            ) : null}
          </div>
        ) : null}
      </Card>

      <Card className="mt-3 p-4">
        <div className="flex items-center justify-between">
          <div className="text-sm font-semibold text-zinc-900">{t("setup.abaTitle")}</div>
          <Badge tone={abaOk ? "green" : "yellow"}>{abaOk ? t("setup.abaFilled") : t("setup.abaPending")}</Badge>
        </div>
        <div className="mt-2 space-y-2">
          <Input value={abaAccount} onChange={(e) => setAbaAccount(e.target.value)} placeholder={t("setup.abaAccount")} />
          <Input value={abaName} onChange={(e) => setAbaName(e.target.value)} placeholder={t("setup.abaName")} />
        </div>
      </Card>

      {err ? (
        <div className="mt-3 rounded-2xl bg-red-50 p-3 text-sm text-red-700">{err}</div>
      ) : null}

      <div className="mt-4 space-y-2">
        <Button
          className="w-full"
          disabled={saving}
          onClick={async () => {
            setSaving(true)
            setErr(null)
            try {
              if (requireField === "aba" && !abaOk) {
                setErr(t("borrow.needAba"))
                return
              }

              if (abaOk) {
                await updateAba(abaAccount.trim(), abaName.trim())
              }
              await refreshMe()

              const me = useAuthStore.getState().user
              if (requireField === "aba") {
                const hasAba = Boolean((me?.aba_account || "").trim()) && Boolean((me?.aba_name || "").trim())
                if (!hasAba) {
                  setErr(t("borrow.needAba"))
                  return
                }
              }

              if (requireField === "phone" && !me?.phone_verified) {
                setErr(t("setup.verifyPhoneFirst"))
                return
              }

              nav(nextPath || "/", { replace: true })
            } catch (e: unknown) {
              if (axios.isAxiosError(e) && !e.response) {
                const origin = window.location.origin
                const base = (api.defaults.baseURL || "").toString()
                setErr(`${t("common.networkError")}\nOrigin: ${origin}\nAPI: ${base}`)
                return
              }
              setErr(errorMessage(e, t("setup.saveFailed")))
            } finally {
              setSaving(false)
            }
          }}
        >
          {saving ? t("common.saving") : requireField === "phone" && !phoneVerified ? t("setup.verifyPhoneFirst") : t("common.saveContinue")}
        </Button>
        <div className="text-xs text-zinc-500">
          {t("setup.securityNote")}
        </div>
      </div>
    </div>
  )
}
