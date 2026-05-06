import WebApp from "@twa-dev/sdk"
import { useMemo } from "react"

export function useTelegram() {
  return useMemo(() => {
    const tg = WebApp
    const user = tg?.initDataUnsafe?.user
    const initData = tg?.initData || ""
    return { tg, user, initData }
  }, [])
}

