import { useMemo, useState } from "react"
import { useNavigate } from "react-router-dom"
import Button from "@/components/ui/Button"
import Card from "@/components/ui/Card"
import { ShieldCheck, HandCoins, Users } from "lucide-react"
import { useAuthStore } from "@/stores/authStore"
import { useI18n } from "@/i18n"
import { updatePreferredLanguage } from "@/api/v1"

export default function Onboarding() {
  const { lang, setLang, t } = useI18n()
  const [i, setI] = useState(0)
  const setOnboardingDone = useAuthStore((s) => s.setOnboardingDone)
  const user = useAuthStore((s) => s.user)
  const nav = useNavigate()

  const [langPicked, setLangPicked] = useState(() => {
    const onboardingDone = localStorage.getItem("khx_onboarding_done") === "1"
    if (onboardingDone) return true
    return localStorage.getItem("khx_lang_selected_v1") === "1"
  })

  if (!langPicked) {
    return (
      <div className="mx-auto flex min-h-screen w-full max-w-md flex-col bg-[#F5F7FA] px-4 py-6">
        <div className="rounded-2xl bg-gradient-to-r from-blue-600 to-cyan-500 p-5 text-white shadow-sm">
          <div className="text-xs opacity-90">{t("onboarding.brand")}</div>
          <div className="mt-1 text-lg font-semibold">{t("langPicker.title")}</div>
          <div className="mt-2 text-sm opacity-90">{t("langPicker.desc")}</div>
        </div>

        <Card className="mt-4 p-4">
          <div className="grid grid-cols-3 gap-2">
            {(["km", "en", "cn"] as const).map((l) => (
              <Button key={l} variant={lang === l ? "primary" : "secondary"} onClick={() => setLang(l)}>
                {t(`lang.${l}`)}
              </Button>
            ))}
          </div>
          <div className="mt-3">
            <Button
              className="w-full"
              onClick={async () => {
                localStorage.setItem("khx_lang_selected_v1", "1")
                setLangPicked(true)
                if (!user) return
                try {
                  await updatePreferredLanguage(lang)
                } catch {
                }
              }}
            >
              {t("langPicker.continue")}
            </Button>
          </div>
        </Card>
      </div>
    )
  }
  const steps = useMemo(() => {
    return [
      { title: t("onboarding.s1.title"), desc: t("onboarding.s1.desc"), icon: ShieldCheck },
      { title: t("onboarding.s2.title"), desc: t("onboarding.s2.desc"), icon: HandCoins },
      { title: t("onboarding.s3.title"), desc: t("onboarding.s3.desc"), icon: Users },
    ]
  }, [t])
  const step = useMemo(() => steps[i], [i, steps])

  return (
    <div className="mx-auto flex min-h-screen w-full max-w-md flex-col bg-[#F5F7FA] px-4 py-6">
      <div className="rounded-2xl bg-gradient-to-r from-blue-600 to-cyan-500 p-5 text-white shadow-sm">
        <div className="text-xs opacity-90">{t("onboarding.brand")}</div>
        <div className="mt-1 text-lg font-semibold">{t("onboarding.title")}</div>
        <div className="mt-2 text-sm opacity-90">{t("onboarding.subtitle")}</div>
      </div>

      <Card className="mt-4 p-4">
        <div className="flex items-center gap-3">
          <div className="flex h-11 w-11 items-center justify-center rounded-2xl bg-blue-50 text-blue-700">
            <step.icon className="h-6 w-6" />
          </div>
          <div>
            <div className="text-sm font-semibold text-zinc-900">{step.title}</div>
            <div className="text-sm text-zinc-600">{step.desc}</div>
          </div>
        </div>

        <div className="mt-4 flex items-center justify-between">
          <div className="text-xs text-zinc-500">{i + 1} / {steps.length}</div>
          <div className="flex gap-2">
            <Button
              variant="secondary"
              size="sm"
              disabled={i === 0}
              onClick={() => setI((v) => Math.max(0, v - 1))}
            >
              {t("onboarding.prev")}
            </Button>
            <Button
              size="sm"
              onClick={() => {
                if (i < steps.length - 1) setI((v) => v + 1)
                else {
                  setOnboardingDone(true)
                  nav("/", { replace: true })
                }
              }}
            >
              {i < steps.length - 1 ? t("onboarding.next") : t("onboarding.start")}
            </Button>
          </div>
        </div>
      </Card>

      <div className="mt-4 text-xs text-zinc-500">
        {t("onboarding.footer")}
      </div>
    </div>
  )
}
