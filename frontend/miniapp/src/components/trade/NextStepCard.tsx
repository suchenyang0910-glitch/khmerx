import Card from "@/components/ui/Card"
import { Clock } from "lucide-react"
import { fmtCountdown } from "@/components/trade/tradeUtils"

export default function NextStepCard({
  title,
  desc,
  deadline,
}: {
  title: string
  desc: string
  deadline?: string | null
}) {
  const cd = fmtCountdown(deadline)
  return (
    <Card className="p-4">
      <div className="flex items-start justify-between gap-3">
        <div>
          <div className="text-sm font-semibold text-zinc-900">{title}</div>
          <div className="mt-1 text-sm text-zinc-600">{desc}</div>
        </div>
        {cd ? (
          <div className="shrink-0 rounded-2xl bg-amber-50 px-3 py-2 text-sm text-amber-900">
            <div className="flex items-center gap-2">
              <Clock className="h-4 w-4" />
              <span>{cd}</span>
            </div>
          </div>
        ) : null}
      </div>
    </Card>
  )
}

