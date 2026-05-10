import { createContext, useCallback, useContext, useMemo, useState } from "react"
import type { ReactNode } from "react"
import { STRINGS, type Lang } from "./strings"

const STORAGE_KEY = "khx_lang"
const MIGRATION_KEY = "khx_lang_migrated_v1"

export const SUPPORTED_LANGS: Lang[] = ["km", "en", "cn"]

export function readStoredLang(): Lang | null {
  if (typeof window === "undefined") return null
  const raw = (localStorage.getItem(STORAGE_KEY) || "").trim()
  if (raw === "km" || raw === "en" || raw === "cn") return raw
  return null
}

export function ensureDefaultLang(): Lang {
  const stored = readStoredLang()
  if (typeof window === "undefined") return stored || "km"

  const migrated = localStorage.getItem(MIGRATION_KEY) === "1"
  if (stored) {
    if (!migrated && stored === "cn") {
      localStorage.setItem(STORAGE_KEY, "km")
      localStorage.setItem(MIGRATION_KEY, "1")
      return "km"
    }
    return stored
  }

  localStorage.setItem(STORAGE_KEY, "km")
  return "km"
}

export function setLang(lang: Lang) {
  if (typeof window === "undefined") return
  localStorage.setItem(STORAGE_KEY, lang)
}

function format(template: string, vars?: Record<string, string | number>) {
  if (!vars) return template
  return template.replace(/\{\{\s*(\w+)\s*\}\}/g, (_, k) => {
    const v = vars[k]
    return v == null ? "" : String(v)
  })
}

export function translate(lang: Lang, key: string, vars?: Record<string, string | number>) {
  const dict = STRINGS[lang]
  const km = STRINGS.km
  const cn = STRINGS.cn
  const text = dict[key] ?? km[key] ?? cn[key] ?? key
  return format(text, vars)
}

type I18nValue = {
  lang: Lang
  setLang: (lang: Lang) => void
  t: (key: string, vars?: Record<string, string | number>) => string
}

const I18nContext = createContext<I18nValue | null>(null)

export function I18nProvider({ children }: { children: ReactNode }) {
  const [lang, setLangState] = useState<Lang>(() => ensureDefaultLang())

  const setLangSafe = useCallback((next: Lang) => {
    setLang(next)
    setLangState(next)
  }, [])

  const value = useMemo<I18nValue>(() => {
    return {
      lang,
      setLang: setLangSafe,
      t: (key, vars) => translate(lang, key, vars),
    }
  }, [lang, setLangSafe])

  return <I18nContext.Provider value={value}>{children}</I18nContext.Provider>
}

export function useI18n() {
  const ctx = useContext(I18nContext)
  if (!ctx) throw new Error("useI18n must be used within I18nProvider")
  return ctx
}
