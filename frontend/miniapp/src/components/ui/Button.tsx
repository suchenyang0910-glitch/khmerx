import type { ButtonHTMLAttributes } from "react"
import { cn } from "@/lib/utils"

type Props = ButtonHTMLAttributes<HTMLButtonElement> & {
  variant?: "primary" | "secondary" | "ghost" | "danger"
  size?: "sm" | "md"
}

export default function Button({
  className,
  variant = "primary",
  size = "md",
  ...props
}: Props) {
  return (
    <button
      className={cn(
        "inline-flex items-center justify-center rounded-xl font-medium transition-colors disabled:opacity-50 disabled:pointer-events-none",
        size === "md" ? "h-12 px-4 text-sm" : "h-9 px-3 text-sm",
        variant === "primary" && "bg-blue-600 text-white hover:bg-blue-700",
        variant === "secondary" && "bg-white text-zinc-900 border border-zinc-200 hover:bg-zinc-50",
        variant === "ghost" && "bg-transparent text-zinc-700 hover:bg-zinc-100",
        variant === "danger" && "bg-red-500 text-white hover:bg-red-600",
        className,
      )}
      {...props}
    />
  )
}

