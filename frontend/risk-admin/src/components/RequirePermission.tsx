import { Navigate, Outlet, useLocation } from 'react-router-dom'
import { useRbacStore } from '@/stores/rbacStore'

export default function RequirePermission(props: { permKey: string }) {
  const permissions = useRbacStore((s) => s.permissions)
  const hydrated = useRbacStore((s) => s.hydrated)
  const location = useLocation()

  if (!hydrated) {
    return <div className="p-4 text-sm text-zinc-600">加载权限中…</div>
  }

  if (!permissions.includes(props.permKey)) {
    return <Navigate to="/forbidden" replace state={{ from: location.pathname }} />
  }

  return <Outlet />
}

