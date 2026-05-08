import Card from "@/components/ui/Card"
import { useI18n } from "@/i18n"

export default function TradeStepper({ index }: { index: number }) {
  const { t } = useI18n()
  return (
    <Card className="p-4">
      <div className="text-sm font-semibold text-zinc-900">{t("trade.stepperTitle")}</div>
      <div className="mt-3 grid grid-cols-5 gap-2 text-center text-xs">
        {[t("trade.step.match"), t("trade.step.transfer"), t("trade.step.confirm"), t("trade.step.repay"), t("trade.step.done")].map((s, i) => {
          const active = index >= i + 1
          return (
            <div key={s} className="space-y-1">
              <div className={active ? "h-2 rounded-full bg-blue-600" : "h-2 rounded-full bg-zinc-200"} />
              <div className={active ? "text-blue-700" : "text-zinc-500"}>{s}</div>
            </div>
          )
        })}
      </div>
    </Card>
  )
}
