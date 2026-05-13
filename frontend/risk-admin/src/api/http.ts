import { useAuthStore } from '@/stores/authStore'
import { useRbacStore } from '@/stores/rbacStore'

export type ApiError = {
  message: string
  status?: number
  url?: string
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
  }).catch((e: unknown) => {
    const err: ApiError = {
      message: (e && typeof e === 'object' && 'message' in e && typeof (e as any).message === 'string') ? (e as any).message : 'network_error',
      url: input,
    }
    throw err
  })

  if (resp.status === 401) {
    useAuthStore.getState().logout()
    useRbacStore.getState().clear()
  }

  if (!resp.ok) {
    const contentType = resp.headers.get('content-type') || ''
    let message = ''
    if (contentType.includes('application/json')) {
      try {
        const data = (await resp.json()) as any
        if (data && typeof data === 'object') {
          if (typeof data.message === 'string') message = data.message
          else if (typeof data.code === 'string') message = data.code
        }
      } catch {
      }
    }
    if (!message) {
      const text = await resp.text().catch(() => '')
      message = text
    }
    const err: ApiError = {
      message: message || resp.statusText || `http_${resp.status}`,
      status: resp.status,
      url: input,
    }
    throw err
  }

  const contentType = resp.headers.get('content-type') || ''
  if (contentType.includes('application/json')) {
    return (await resp.json()) as T
  }
  return (await resp.text()) as unknown as T
}
