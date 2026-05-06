import { useMemo, useState } from "react"
import { useNavigate } from "react-router-dom"
import Button from "@/components/ui/Button"
import Card from "@/components/ui/Card"
import { ShieldCheck, HandCoins, Users } from "lucide-react"
import { useAuthStore } from "@/stores/authStore"

const steps = [
  {
    title: "什么是 KhmerX",
    desc: "KhmerX 是本地信任的 P2P 微借贷撮合系统，让借款与出借更透明。",
    icon: ShieldCheck,
  },
  {
    title: "如何借钱",
    desc: "选择金额与期限 → 生成挂单 → 出借人接单 → 双方确认 → 按期还款。",
    icon: HandCoins,
  },
  {
    title: "安全说明",
    desc: "平台不主动私聊、不批量拉群；所有通知必须由你触发或订阅；关键步骤都有记录。",
    icon: Users,
  },
]

export default function Onboarding() {
  const [i, setI] = useState(0)
  const setOnboardingDone = useAuthStore((s) => s.setOnboardingDone)
  const nav = useNavigate()
  const step = useMemo(() => steps[i], [i])

  return (
    <div className="mx-auto flex min-h-screen w-full max-w-md flex-col bg-[#F5F7FA] px-4 py-6">
      <div className="rounded-2xl bg-gradient-to-r from-blue-600 to-cyan-500 p-5 text-white shadow-sm">
        <div className="text-xs opacity-90">KhmerX Mini App</div>
        <div className="mt-1 text-lg font-semibold">金融 + 本地信任 + 现代科技</div>
        <div className="mt-2 text-sm opacity-90">3 屏了解清楚，避免迷路与纠纷</div>
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
              上一页
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
              {i < steps.length - 1 ? "下一页" : "开始使用"}
            </Button>
          </div>
        </div>
      </Card>

      <div className="mt-4 text-xs text-zinc-500">
        继续即表示你理解：借款会显示“实际到账/到期需还”，并以双方确认与凭证为准。
      </div>
    </div>
  )
}

