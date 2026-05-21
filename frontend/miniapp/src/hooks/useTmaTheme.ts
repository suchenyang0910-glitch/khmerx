import { useEffect } from "react"
import WebApp from "@twa-dev/sdk"

function applyThemeVars(tg: typeof WebApp) {
  const root = document.documentElement
  const p = (tg?.themeParams || {}) as {
    bg_color?: string
    text_color?: string
    hint_color?: string
    link_color?: string
    button_color?: string
    button_text_color?: string
    secondary_bg_color?: string
  }
  const entries: Array<[string, string | undefined]> = [
    ["--tg-bg", p.bg_color],
    ["--tg-text", p.text_color],
    ["--tg-hint", p.hint_color],
    ["--tg-link", p.link_color],
    ["--tg-button", p.button_color],
    ["--tg-button-text", p.button_text_color],
    ["--tg-secondary-bg", p.secondary_bg_color],
  ]
  for (const [k, v] of entries) {
    if (typeof v === "string" && v.trim()) root.style.setProperty(k, v)
  }
  try {
    root.style.setProperty("--tg-viewport-height", `${tg.viewportHeight || window.innerHeight}px`)
  } catch {
    void 0
  }
}

export function useTmaTheme() {
  useEffect(() => {
    const tg = WebApp
    if (!tg) return
    try {
      tg.ready()
      tg.expand()
    } catch {
      void 0
    }
    applyThemeVars(tg)
    const onTheme = () => applyThemeVars(tg)
    const onViewport = () => applyThemeVars(tg)
    try {
      tg.onEvent("themeChanged", onTheme)
      tg.onEvent("viewportChanged", onViewport)
    } catch {
      void 0
    }
    return () => {
      try {
        tg.offEvent("themeChanged", onTheme)
        tg.offEvent("viewportChanged", onViewport)
      } catch {
        void 0
      }
    }
  }, [])
}
