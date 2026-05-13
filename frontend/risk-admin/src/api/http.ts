import { useAuthStore } from '@/stores/authStore'
import { useRbacStore } from '@/stores/rbacStore'

export type ApiError = {
  message: string
  status?: number
}

export function getErrorMessage(err: unknown): string {
  if (typeof err === 'string') return err
  if (err && typeof err === 'object' && 'message' in err) {
    const m = (err as { message?: unknown }).message
    if (typeof m === 'string' && m) return m
  }
  return '请求失败'
}

export async function requestJson<T>(input: string, init?: RequestInit): Promise<T> {
  const token = useAuthStore.getState().token
  const headers = new Headers(init?.headers)
  headers.set('Accept', 'application/json')
  if (!headers.has('Content-Type') && init?.body != null) {
    headers.set('Content-Type', 'application/json')
  }
  if (token) {
    headers.set('Authorization', `Bearer ${token}`)
  }

  const resp = await fetch(input, {
    ...init,
    headers,
  })

  if (resp.status === 401) {
    useAuthStore.getState().logout()
    useRbacStore.getState().clear()
  }

  if (!resp.ok) {
    const text = await resp.text().catch(() => '')
    const err: ApiError = {
      message: text || resp.statusText || 'request_failed',
      status: resp.status,
    }
    throw err
  }

  const contentType = resp.headers.get('content-type') || ''
  if (contentType.includes('application/json')) {
    return (await resp.json()) as T
  }
  return (await resp.text()) as unknown as T
}
