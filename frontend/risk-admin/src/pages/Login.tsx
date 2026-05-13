import { useMemo, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { getErrorMessage, requestJson } from '@/api/http'
import type { MeResponse, TokenResponse } from '@/api/types'
import { useAuthStore } from '@/stores/authStore'
import { useRbacStore } from '@/stores/rbacStore'
import { KeyRound } from 'lucide-react'

export default function Login() {
  const [merchantId, setMerchantId] = useState('m_demo')
  const [apiKey, setApiKey] = useState('demo_key')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const setSession = useAuthStore((s) => s.setSession)
  const setMe = useRbacStore((s) => s.setMe)
  const clear = useRbacStore((s) => s.clear)
  const navigate = useNavigate()

  const authHint = useMemo(() => {
    if (import.meta.env.PROD) {
      return `${window.location.origin}/api-auth → auth-service`
    }
    const base = import.meta.env.VITE_AUTH_BASE_URL || 'http://localhost:8081'
    return `${base} (dev proxy: /api-auth)`
  }, [])

  async function onSubmit(e: React.FormEvent) {
    e.preventDefault()
    setError(null)
    setLoading(true)
    try {
      const resp = await requestJson<TokenResponse>('/api-auth/auth/token', {
        method: 'POST',
        body: JSON.stringify({ merchantId, apiKey }),
      })
      setSession(resp.accessToken, merchantId)
      clear()
      const me = await requestJson<MeResponse>('/api-risk/system/me')
      setMe(me)
      navigate('/')
    } catch (err: unknown) {
      setError(getErrorMessage(err))
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-dvh bg-zinc-50 text-zinc-900">
      <div className="mx-auto flex min-h-dvh max-w-md items-center px-4">
        <div className="w-full rounded-2xl border border-zinc-200 bg-white p-6 shadow-sm">
          <div className="flex items-center gap-3">
            <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-zinc-900 text-white">
              <KeyRound className="h-5 w-5" />
            </div>
            <div className="min-w-0">
              <div className="truncate text-base font-semibold">风控平台管理后台</div>
              <div className="truncate text-xs text-zinc-500">Auth: {authHint}</div>
            </div>
          </div>

          <form className="mt-6 space-y-4" onSubmit={onSubmit}>
            <div>
              <label className="block text-sm font-medium text-zinc-700">商户 ID</label>
              <input
                value={merchantId}
                onChange={(e) => setMerchantId(e.target.value)}
                className="mt-1 w-full rounded-lg border border-zinc-200 bg-white px-3 py-2 text-sm outline-none ring-0 transition focus:border-zinc-400"
                placeholder="例如：m_demo"
                autoComplete="username"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-zinc-700">API Key</label>
              <input
                value={apiKey}
                onChange={(e) => setApiKey(e.target.value)}
                className="mt-1 w-full rounded-lg border border-zinc-200 bg-white px-3 py-2 text-sm outline-none ring-0 transition focus:border-zinc-400"
                placeholder="例如：demo_key"
                autoComplete="current-password"
              />
            </div>

            {error ? (
              <div className="rounded-lg border border-red-200 bg-red-50 px-3 py-2 text-sm text-red-700">{error}</div>
            ) : null}

            <button
              type="submit"
              disabled={loading || !merchantId || !apiKey}
              className="inline-flex w-full items-center justify-center rounded-lg bg-zinc-900 px-3 py-2 text-sm font-medium text-white transition hover:bg-zinc-800 disabled:cursor-not-allowed disabled:opacity-50"
            >
              {loading ? '登录中…' : '登录'}
            </button>
          </form>

          <div className="mt-4 text-xs text-zinc-500">
            本版本使用商户 API Key 获取 JWT。后续可替换为管理员账号/SSO。
          </div>
        </div>
      </div>
    </div>
  )
}
