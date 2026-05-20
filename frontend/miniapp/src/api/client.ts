import axios from "axios"
import { ensureDefaultLang } from "@/i18n"
import type { AxiosRequestHeaders } from "axios"

function resolveApiBaseURL() {
  const envBase = (import.meta.env.VITE_API_BASE_URL as string | undefined) || ""
  if (envBase.trim()) return envBase.trim()

  if (typeof window !== "undefined") {
    const stored = localStorage.getItem("khx_dev_api_base")

    if (import.meta.env.DEV) {
      if (stored && /^https?:\/\//.test(stored)) {
        try {
          const u = new URL(stored)
          const h = window.location.hostname
          const isLocal = (x: string) => x === "localhost" || x === "127.0.0.1"
          if (u.hostname === h || (isLocal(u.hostname) && isLocal(h))) {
            return stored
          }
        } catch {
        }
      }
      return ""
    }

    if (stored && /^https?:\/\//.test(stored)) return stored

    const host = window.location.hostname
    const isProdDomain = host === "api.khmerx.org" || host.endsWith(".khmerx.org")
    if (!isProdDomain) {
      if (host === "localhost" || host === "127.0.0.1") {
        return "http://127.0.0.1:3040"
      }
      const protocol = window.location.protocol === "https:" ? "https:" : "http:"
      return `${protocol}//${host}:3040`
    }
  }

  return "https://api.khmerx.org"
}

const rawBase = resolveApiBaseURL()
const rootURL = rawBase.replace(/\/api\/v1\/?$/, "").replace(/\/$/, "")

export const api = axios.create({
  baseURL: rootURL,
  timeout: 20000,
})

export const apiV1 = axios.create({
  baseURL: `${rootURL.replace(/\/$/, "")}/api/v1`,
  timeout: 20000,
})

api.interceptors.request.use((config) => {
  const lang = ensureDefaultLang()
  const next = {
    ...((config.headers ?? {}) as Record<string, string>),
    "X-Lang": lang,
  } as unknown as AxiosRequestHeaders
  config.headers = next
  return config
})

apiV1.interceptors.request.use((config) => {
  const lang = ensureDefaultLang()
  const initData = localStorage.getItem("khx_tma_init_data")
  if (initData) {
    const next = {
      ...((config.headers ?? {}) as Record<string, string>),
      Authorization: `TMA ${initData}`,
      "X-Lang": lang,
    } as unknown as AxiosRequestHeaders
    config.headers = next
  } else {
    const next = {
      ...((config.headers ?? {}) as Record<string, string>),
      "X-Lang": lang,
    } as unknown as AxiosRequestHeaders
    config.headers = next
  }
  return config
})
