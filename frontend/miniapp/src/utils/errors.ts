import type { AxiosError } from "axios"

export function errorMessage(e: unknown, fallback = "请求失败") {
  if (typeof e === "string") return e
  if (!e || typeof e !== "object") return fallback

  const ae = e as AxiosError<unknown>
  const data = ae.response?.data
  if (data && typeof data === "object") {
    const detail = (data as Record<string, unknown>).detail
    if (typeof detail === "string") return detail
    if (detail != null) return JSON.stringify(detail)
  }
  if (typeof ae.message === "string" && ae.message) return ae.message
  return fallback
}
