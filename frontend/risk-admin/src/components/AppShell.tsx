import { NavLink, Outlet, useLocation, useNavigate } from 'react-router-dom'
import { LayoutDashboard, ShieldAlert, SlidersHorizontal, LogOut, Settings } from 'lucide-react'
import { useAuthStore } from '@/stores/authStore'
import { useRbacStore } from '@/stores/rbacStore'
import { cn } from '@/lib/utils'

const navItems = [
  { to: '/', label: '控制台', icon: LayoutDashboard, perm: null },
  { to: '/rules', label: '规则管理', icon: SlidersHorizontal, perm: 'rules.read' },
  { to: '/cases', label: '命中处置', icon: ShieldAlert, perm: 'cases.read' },
  { to: '/system', label: '系统管理', icon: Settings, perm: 'system.read' },
]

export default function AppShell() {
  const merchantId = useAuthStore((s) => s.merchantId)
  const logout = useAuthStore((s) => s.logout)
  const clear = useRbacStore((s) => s.clear)
  const permissions = useRbacStore((s) => s.permissions)
  const navigate = useNavigate()
  const location = useLocation()

  return (
    <div className="min-h-dvh bg-zinc-50 text-zinc-900">
      <div className="flex min-h-dvh">
        <aside className="w-64 shrink-0 border-r border-zinc-200 bg-white">
          <div className="flex h-14 items-center gap-2 px-4">
            <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-zinc-900 text-white">
              RX
            </div>
            <div className="min-w-0">
              <div className="truncate text-sm font-semibold">风控平台</div>
              <div className="truncate text-xs text-zinc-500">管理后台</div>
            </div>
          </div>
          <nav className="px-2 pb-4">
            {navItems
              .filter((item) => !item.perm || permissions.includes(item.perm))
              .map((item) => {
              const Icon = item.icon
              return (
                <NavLink
                  key={item.to}
                  to={item.to}
                  className={({ isActive }) =>
                    cn(
                      'mt-1 flex items-center gap-2 rounded-lg px-3 py-2 text-sm transition-colors',
                      isActive
                        ? 'bg-zinc-900 text-white'
                        : 'text-zinc-700 hover:bg-zinc-100 hover:text-zinc-900'
                    )
                  }
                  end={item.to === '/'}
                >
                  <Icon className="h-4 w-4" />
                  <span className="truncate">{item.label}</span>
                </NavLink>
              )
            })}
          </nav>
        </aside>

        <div className="flex min-w-0 flex-1 flex-col">
          <header className="sticky top-0 z-10 flex h-14 items-center justify-between border-b border-zinc-200 bg-white px-4">
            <div className="min-w-0">
              <div className="truncate text-sm font-medium text-zinc-900">
                {location.pathname === '/' ? '控制台' : null}
                {location.pathname === '/rules' ? '规则管理' : null}
                {location.pathname === '/cases' ? '命中处置' : null}
                {location.pathname === '/system' ? '系统管理' : null}
              </div>
              <div className="truncate text-xs text-zinc-500">{merchantId ? `merchant: ${merchantId}` : ''}</div>
            </div>

            <button
              type="button"
              onClick={() => {
                logout()
                clear()
                navigate('/login')
              }}
              className="inline-flex items-center gap-2 rounded-lg border border-zinc-200 bg-white px-3 py-2 text-sm text-zinc-700 transition-colors hover:bg-zinc-50"
            >
              <LogOut className="h-4 w-4" />
              退出
            </button>
          </header>

          <main className="min-w-0 flex-1 p-4">
            <Outlet />
          </main>
        </div>
      </div>
    </div>
  )
}
