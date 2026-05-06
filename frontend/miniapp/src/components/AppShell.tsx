import { useEffect, useMemo, useState } from "react"
import { Navigate, Outlet, useLocation } from "react-router-dom"
import TabBar from "@/components/TabBar"
import Button from "@/components/ui/Button"
import { useTelegram } from "@/hooks/useTelegram"
import { useAuthStore } from "@/stores/authStore"
import type { AppUser } from "@/api/types"
import { api } from "@/api/client"
import axios from "axios"

function needsProfile(user: AppUser | null) {
  const phoneOk = Boolean((user?.phone || "").trim()) && Boolean(user?.phone_verified)
  const abaOk = Boolean((user?.aba_account || "").trim()) && Boolean((user?.aba_name || "").trim())
  return !(phoneOk && abaOk)
}

export default function AppShell() {
  const { initData, tg } = useTelegram()
  const { pathname } = useLocation()
  const booting = useAuthStore((s) => s.booting)
  const error = useAuthStore((s) => s.error)
  const user = useAuthStore((s) => s.user)
  const risk = useAuthStore((s) => s.risk)
  const onboardingDone = useAuthStore((s) => s.onboardingDone)
  const bootstrap = useAuthStore((s) => s.bootstrap)
  const storedInitData = useAuthStore((s) => s.initData)

  const [devBooting, setDevBooting] = useState(false)
  const [devError, setDevError] = useState<string | null>(null)
  const [autoDevAttempted, setAutoDevAttempted] = useState(false)
  const canDevBoot = useMemo(() => {
    const host = window.location.hostname
    return host === "127.0.0.1" || host === "localhost"
  }, [])

  useEffect(() => {
    tg?.expand()
    tg?.enableClosingConfirmation()
  }, [tg])

  async function getDevInitData() {
    const tgId = 90000000 + Math.floor(Math.random() * 1000000)
    try {
      const res = await api.get<{ ok: boolean; data: { init_data: string } }>("/auth/dev-tma", {
        params: { tg_id: tgId },
      })
      return res.data?.data?.init_data || ""
    } catch (e: any) {
      const status = e?.response?.status
      if (status === 500) {
        const detail = e?.response?.data?.detail
        if (typeof detail === "string" && detail.toLowerCase().includes("bot token")) {
          throw new Error("后端未配置 BOT_TOKENS：请在后端 .env 设置 BOT_TOKENS=... 并重启")
        }
      }
      if (status === 404) {
        throw new Error("本地调试接口未开启：请在后端设置 DEV_TMA_ENABLED=true 并重启后端")
      }

      const bases = [
        localStorage.getItem("khx_dev_api_base") || "",
        "http://127.0.0.1:3040",
        "http://127.0.0.1:3030",
      ].filter(Boolean)
      for (const b of bases) {
        try {
          const r = await axios.get<{ ok: boolean; data: { init_data: string } }>(`${b}/auth/dev-tma`, {
            params: { tg_id: tgId },
            timeout: 8000,
          })
          const init = r.data?.data?.init_data || ""
          if (init) {
            localStorage.setItem("khx_dev_api_base", b)
            return init
          }
        } catch {
        }
      }

      throw new Error("无法连接后端：请先启动后端（建议 3040）：python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 3040")
    }
  }

  useEffect(() => {
    if (user) return
    if (!booting || error) return
    const data = initData || storedInitData
    if (!data && canDevBoot && !autoDevAttempted) {
      setAutoDevAttempted(true)
      setDevBooting(true)
      setDevError(null)
      getDevInitData()
        .then((devInit) => bootstrap(devInit))
        .catch((e) => {
          setDevError(e instanceof Error ? e.message : "本地登录失败")
          return bootstrap("")
        })
        .finally(() => setDevBooting(false))
      return
    }

    bootstrap(data)
  }, [bootstrap, initData, storedInitData, user, booting, error, canDevBoot, autoDevAttempted])

  if (!onboardingDone) {
    return <Navigate to="/onboarding" replace />
  }

  if (booting) {
    return (
      <div className="mx-auto flex min-h-screen w-full max-w-md flex-col bg-[#F5F7FA]">
        <div className="p-4">
          <div className="rounded-2xl bg-gradient-to-r from-blue-600 to-cyan-500 p-4 text-white shadow-sm">
            <div className="text-sm opacity-90">KhmerX</div>
            <div className="mt-1 text-lg font-semibold">正在加载你的账户…</div>
          </div>
          <div className="mt-4 space-y-3">
            <div className="h-20 animate-pulse rounded-2xl bg-white" />
            <div className="h-24 animate-pulse rounded-2xl bg-white" />
            <div className="h-24 animate-pulse rounded-2xl bg-white" />
          </div>
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="mx-auto flex min-h-screen w-full max-w-md flex-col bg-[#F5F7FA] p-4">
        <div className="rounded-2xl bg-white p-4 shadow-sm">
          <div className="text-sm font-semibold text-zinc-900">无法登录</div>
          <div className="mt-2 text-sm text-zinc-600">{error}</div>
          <div className="mt-4">
            <Button onClick={() => window.location.reload()} className="w-full">刷新重试</Button>
          </div>

          {canDevBoot ? (
            <div className="mt-3 grid grid-cols-2 gap-2">
              <Button
                variant="secondary"
                onClick={() => {
                  localStorage.setItem("khx_dev_api_base", "http://127.0.0.1:3040")
                  window.location.reload()
                }}
              >
                切到 3040
              </Button>
              <Button
                variant="secondary"
                onClick={() => {
                  localStorage.setItem("khx_dev_api_base", "http://127.0.0.1:3030")
                  window.location.reload()
                }}
              >
                切到 3030
              </Button>
            </div>
          ) : null}

          {canDevBoot ? (
            <div className="mt-3">
              <Button
                variant="secondary"
                disabled={devBooting}
                onClick={async () => {
                  setDevBooting(true)
                  setDevError(null)
                  try {
                    const devInit = await getDevInitData()
                    await bootstrap(devInit)
                  } catch (e) {
                    setDevError(e instanceof Error ? e.message : "本地登录失败")
                  } finally {
                    setDevBooting(false)
                  }
                }}
                className="w-full"
              >
                {devBooting ? "正在生成本地测试账号…" : "本地调试：生成测试账号"}
              </Button>
              {devError ? <div className="mt-2 text-xs text-amber-700">{devError}</div> : null}
            </div>
          ) : null}
        </div>
      </div>
    )
  }

  if (user && needsProfile(user) && pathname !== "/setup") {
    return <Navigate to="/setup" replace />
  }

  const blocked = risk?.risk_level && ["blocked", "restricted"].includes(risk.risk_level)

  return (
    <div className="mx-auto flex min-h-screen w-full max-w-md flex-col bg-[#F5F7FA]">
      <header className="sticky top-0 z-30 border-b border-zinc-200 bg-white/90 backdrop-blur">
        <div className="flex items-center justify-between px-4 py-3">
          <div>
            <div className="text-xs text-zinc-500">Verified · Trusted · Secure</div>
            <div className="text-sm font-semibold text-zinc-900">KhmerX</div>
          </div>
          <div className="text-xs text-zinc-600">{user?.name || ""}</div>
        </div>
        {blocked ? (
          <div className="px-4 pb-3">
            <div className="rounded-2xl bg-amber-50 p-3 text-sm text-amber-900">
              你的账户当前受限，部分操作已关闭。请在“我的”查看原因。
            </div>
          </div>
        ) : null}
      </header>

      <main className="flex-1 px-4 pb-24 pt-4">
        <Outlet />
      </main>

      <TabBar />
    </div>
  )
}
