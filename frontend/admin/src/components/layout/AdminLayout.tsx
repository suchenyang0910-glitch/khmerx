import { Outlet, NavLink, useNavigate } from "react-router-dom"
import { BarChart3, Bell, DollarSign, LogOut, Settings, TrendingUp, Megaphone, Scale, ShieldAlert, ShieldCheck, Users } from "lucide-react"
import { useAdminAuthStore } from "@/stores/adminAuthStore"
import clsx from "clsx"

const nav = [
  { to: "/", label: "仪表盘", icon: BarChart3 },
  { to: "/reports", label: "报表", icon: TrendingUp },
  { to: "/users", label: "用户", icon: Users },
  { to: "/offers", label: "挂单", icon: ShieldAlert },
  { to: "/trades", label: "交易", icon: ShieldAlert },
  { to: "/risk/events", label: "风控事件", icon: ShieldCheck },
  { to: "/risk/rules", label: "风控规则", icon: ShieldCheck },
  { to: "/disputes", label: "争议", icon: Scale },
  { to: "/notifications", label: "通知", icon: Bell },
  { to: "/announcements", label: "公告", icon: Megaphone },
  { to: "/config", label: "配置", icon: Settings },
  { to: "/interest-rates", label: "利率矩阵", icon: DollarSign },
]

export function AdminLayout() {
  const username = useAdminAuthStore((s) => s.username)
  const logout = useAdminAuthStore((s) => s.logout)
  const navg = useNavigate()

  return (
    <div className="min-h-screen bg-zinc-950 text-zinc-100">
      <div className="mx-auto flex max-w-7xl">
        <aside className="hidden w-64 flex-none border-r border-zinc-800 bg-zinc-950 md:block">
          <div className="px-5 py-5">
            <div className="text-lg font-semibold">KhmerX Admin</div>
            <div className="mt-1 text-xs text-zinc-400">{username ? `@${username}` : ""}</div>
          </div>
          <nav className="px-3 pb-6">
            {nav.map((item) => {
              const Icon = item.icon
              return (
                <NavLink
                  key={item.to}
                  to={item.to}
                  end={item.to === "/"}
                  className={({ isActive }) =>
                    clsx(
                      "mb-1 flex items-center gap-3 rounded-xl px-3 py-2 text-sm",
                      isActive ? "bg-zinc-800 text-white" : "text-zinc-300 hover:bg-zinc-900"
                    )
                  }
                >
                  <Icon className="h-4 w-4" />
                  {item.label}
                </NavLink>
              )
            })}
          </nav>
        </aside>

        <div className="min-w-0 flex-1">
          <header className="sticky top-0 z-10 border-b border-zinc-800 bg-zinc-950/90 backdrop-blur">
            <div className="flex items-center justify-between px-5 py-4">
              <div className="text-sm text-zinc-400">运营后台</div>
              <button
                className="inline-flex items-center gap-2 rounded-xl border border-zinc-800 bg-zinc-900 px-3 py-2 text-sm text-zinc-200 hover:bg-zinc-800"
                onClick={() => {
                  logout()
                  navg("/login", { replace: true })
                }}
              >
                <LogOut className="h-4 w-4" />
                退出
              </button>
            </div>
          </header>

          <main className="px-5 py-6">
            <Outlet />
          </main>
        </div>
      </div>
    </div>
  )
}
