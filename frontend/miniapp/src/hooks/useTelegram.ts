import WebApp from "@twa-dev/sdk"
import { useEffect, useState } from "react"

function readInitDataFromUrl(): string {
  if (typeof window === "undefined") return ""
  try {
    const u = new URL(window.location.href)
    const q = u.searchParams.get("tgWebAppData") || ""
    if (q) return q
  } catch {
    return ""
  }
  return ""
}

export function useTelegram() {
  const [initData, setInitData] = useState<string>(() => {
    return WebApp?.initData || localStorage.getItem("khx_tma_init_data") || readInitDataFromUrl() || ""
  })
  const [user, setUser] = useState<unknown>(() => WebApp?.initDataUnsafe?.user)

  useEffect(() => {
    let tries = 0
    let alive = true
    let lastInit = initData
    let lastUser = user

    const tick = () => {
      if (!alive) return
      tries += 1
      try {
        WebApp?.ready?.()
      } catch {
        void 0
      }

      const nextInit = WebApp?.initData || readInitDataFromUrl() || ""
      if (nextInit && nextInit !== lastInit) {
        lastInit = nextInit
        setInitData(nextInit)
      }

      const nextUser = WebApp?.initDataUnsafe?.user
      if (nextUser && nextUser !== lastUser) {
        lastUser = nextUser
        setUser(nextUser)
      }

      if (tries < 10 && !nextInit) {
        window.setTimeout(tick, 200)
      }
    }

    tick()
    return () => {
      alive = false
    }
  }, [])

  return { tg: WebApp, user, initData }
}

