import { NavLink } from "react-router-dom"
import { cn } from "@/lib/utils"
import { Home, HandCoins, Landmark, ListChecks, User } from "lucide-react"

const items = [
  { to: "/", label: "首页", icon: Home },
  { to: "/borrow", label: "借款", icon: HandCoins },
  { to: "/lend", label: "出借", icon: Landmark },
  { to: "/trades", label: "交易", icon: ListChecks },
  { to: "/me", label: "我的", icon: User },
]

export default function TabBar() {
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

