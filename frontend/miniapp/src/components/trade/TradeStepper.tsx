import Card from "@/components/ui/Card"

export default function TradeStepper({ index }: { index: number }) {
  return (
    <Card className="p-4">
      <div className="text-sm font-semibold text-zinc-900">状态进度</div>
      <div className="mt-3 grid grid-cols-5 gap-2 text-center text-xs">
        {["匹配", "打款", "确认", "还款", "完成"].map((s, i) => {
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

