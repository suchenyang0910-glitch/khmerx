import axios from "axios"

function resolveApiBaseURL() {
  const envBase = (import.meta.env.VITE_API_BASE_URL as string | undefined) || ""
  if (envBase.trim()) return envBase.trim()

  if (typeof window !== "undefined") {
    const stored = localStorage.getItem("khx_dev_api_base")
    if (stored && /^https?:\/\//.test(stored)) return stored

    const host = window.location.hostname
    if (host === "localhost" || host === "127.0.0.1") {
      return "http://127.0.0.1:3040"
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

apiV1.interceptors.request.use((config) => {
  const initData = localStorage.getItem("khx_tma_init_data")
  if (initData) {
    config.headers = {
      ...(config.headers as any),
      Authorization: `TMA ${initData}`,
    } as any
  }
  return config
})
