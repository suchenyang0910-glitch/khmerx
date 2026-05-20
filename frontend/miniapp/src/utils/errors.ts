import type { AxiosError } from "axios"

export function errorMessage(e: unknown, fallback = "Request failed") {
  if (typeof e === "string") return e
  if (!e || typeof e !== "object") return fallback

  const ae = e as AxiosError<unknown>
  const data = ae.response?.data
  if (typeof data === "string" && data.trim()) return data
  if (data && typeof data === "object") {
    const message = (data as Record<string, unknown>).message
    const code = (data as Record<string, unknown>).code
    if (typeof message === "string" && message.trim()) {
      if (typeof code === "string" && code.trim()) return `${message} (${code})`
      return message
    }
    const detail = (data as Record<string, unknown>).detail
    if (typeof detail === "string") return detail
    if (detail != null) return JSON.stringify(detail)
  }
  if (typeof ae.message === "string" && ae.message) return ae.message
  return fallback
}
