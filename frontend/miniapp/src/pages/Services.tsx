import { Link } from "react-router-dom"
import Card from "@/components/ui/Card"
import Button from "@/components/ui/Button"
import { useI18n } from "@/i18n"
import { HandCoins, Smartphone, ShoppingCart } from "lucide-react"

const services = [
  {
    bizType: "lease" as const,
    icon: Smartphone,
    titleKey: "services.lease.title",
    descKey: "services.lease.desc",
  },
  {
    bizType: "installment" as const,
    icon: ShoppingCart,
    titleKey: "services.installment.title",
    descKey: "services.installment.desc",
  },
  {
    bizType: "pledge" as const,
    icon: HandCoins,
    titleKey: "services.pledge.title",
    descKey: "services.pledge.desc",
  },
]

export default function Services() {
  const { t } = useI18n()

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <div className="text-base font-semibold text-zinc-900">{t("services.title")}</div>
        <Link to="/applications" className="text-sm text-blue-600">
          {t("services.my")}
        </Link>
      </div>

      <div className="grid gap-3">
        {services.map((s) => (
          <Card key={s.bizType} className="p-4">
            <div className="flex items-start justify-between gap-3">
              <div>
                <div className="text-sm font-semibold text-zinc-900">{t(s.titleKey)}</div>
                <div className="mt-1 text-sm text-zinc-600">{t(s.descKey)}</div>
              </div>
              <div className="flex h-10 w-10 items-center justify-center rounded-2xl bg-blue-50 text-blue-700">
                <s.icon className="h-5 w-5" />
              </div>
            </div>

            <div className="mt-3">
              {s.bizType === "lease" || s.bizType === "installment" ? (
                <Link to={`/catalog/${s.bizType}`}>
                  <Button className="w-full">{t("services.choose")}</Button>
                </Link>
              ) : (
                <Link to={`/apply/${s.bizType}`}>
                  <Button className="w-full">{t("services.apply")}</Button>
                </Link>
              )}
            </div>
          </Card>
        ))}
      </div>
    </div>
  )
}
