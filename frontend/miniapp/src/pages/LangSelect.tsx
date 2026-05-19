import { useState } from "react"
import { useNavigate } from "react-router-dom"
import Button from "@/components/ui/Button"
import Card from "@/components/ui/Card"
import { useI18n } from "@/i18n"

export default function LangSelect() {
  const { lang, setLang, t } = useI18n()
  const [selected, setSelected] = useState(lang)
  const nav = useNavigate()

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
            <Button
              key={l}
              variant={selected === l ? "primary" : "secondary"}
              onClick={() => {
                setSelected(l)
                setLang(l)
              }}
            >
              {t(`lang.${l}`)}
            </Button>
          ))}
        </div>

        <div className="mt-3">
          <Button
            className="w-full"
            onClick={() => {
              localStorage.setItem("khx_lang_selected_v2", "1")
              nav("/", { replace: true })
            }}
          >
            {t("langPicker.continue")}
          </Button>
        </div>
      </Card>
    </div>
  )
}
