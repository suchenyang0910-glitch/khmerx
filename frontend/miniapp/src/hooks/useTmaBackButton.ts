import { useEffect } from "react"
import WebApp from "@twa-dev/sdk"

export function useTmaBackButton(enabled: boolean, onBack: () => void) {
  useEffect(() => {
    const tg = WebApp
    if (!tg?.BackButton) return
    if (!enabled) {
      tg.BackButton.hide()
      return
    }

    const handler = () => onBack()
    tg.BackButton.onClick(handler)
    tg.BackButton.show()
    return () => {
      try {
        tg.BackButton.offClick(handler)
      } catch {
        void 0
      }
      tg.BackButton.hide()
    }
  }, [enabled, onBack])
}

