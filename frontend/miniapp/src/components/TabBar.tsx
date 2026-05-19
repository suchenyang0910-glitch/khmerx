import { NavLink } from "react-router-dom"
import { cn } from "@/lib/utils"
import { Home, HandCoins, Landmark, ListChecks, User } from "lucide-react"
import { useI18n } from "@/i18n"

export default function TabBar() {
  const { t } = useI18n()
  const items = [
    { to: "/", label: t("nav.home"), icon: Home },
    { to: "/borrow", label: t("nav.borrow"), icon: HandCoins },
    { to: "/lend", label: t("nav.lend"), icon: Landmark },
    { to: "/trades", label: t("nav.trades"), icon: ListChecks },
    { to: "/me", label: t("nav.me"), icon: User },
  ]
  return (
    <nav className="fixed inset-x-0 bottom-0 z-40 mx-auto w-full max-w-md border-t border-zinc-200 bg-white/95 backdrop-blur">
      <div className="grid grid-cols-5 px-2 py-2">
        {items.map((it) => (
          <NavLink
            key={it.to}
            to={it.to}
            className={({ isActive }) =>
              cn(
                "flex flex-col items-center justify-center gap-1 rounded-xl py-2 text-xs",
                isActive ? "text-blue-600" : "text-zinc-500",
              )
            }
          >
            <it.icon className="h-5 w-5" />
            <span>{it.label}</span>
          </NavLink>
        ))}
      </div>
    </nav>
  )
}
