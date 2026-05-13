import { Navigate, Outlet, useLocation } from 'react-router-dom'
import { useAuthStore } from '@/stores/authStore'
import { useRbacStore } from '@/stores/rbacStore'
import { useEffect, useState } from 'react'
import { getErrorMessage, requestJson } from '@/api/http'
import type { MeResponse } from '@/api/types'

export default function RequireAuth() {
  const token = useAuthStore((s) => s.token)
  const location = useLocation()
  const hydrated = useRbacStore((s) => s.hydrated)
  const setMe = useRbacStore((s) => s.setMe)
  const clear = useRbacStore((s) => s.clear)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    let mounted = true
    async function loadMe() {
      if (!token) {
        clear()
        return
      }
      if (hydrated) return
      setLoading(true)
      setError(null)
      try {
        const me = await requestJson<MeResponse>('/api-risk/system/me')
        if (mounted) setMe(me)
      } catch (e: unknown) {
        clear()
        if (mounted) setError(getErrorMessage(e))
      } finally {
        if (mounted) setLoading(false)
      }
    }
    loadMe()
    return () => {
      mounted = false
    }
  }, [clear, hydrated, setMe, token])

  if (!token) {
    return <Navigate to="/login" replace state={{ from: location.pathname }} />
  }

  if (!hydrated && loading) {
    return <div className="p-4 text-sm text-zinc-600">加载中…</div>
  }

  if (error) {
    return <div className="p-4 text-sm text-red-700">{error}</div>
  }

  return <Outlet />
}
