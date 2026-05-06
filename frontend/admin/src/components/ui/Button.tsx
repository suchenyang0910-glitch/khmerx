import clsx from "clsx"

export function Button({
  className,
  variant = "primary",
  disabled,
  onClick,
  children,
  type,
}: {
  className?: string
  variant?: "primary" | "secondary" | "ghost"
  disabled?: boolean
  onClick?: () => void
  children: React.ReactNode
  type?: "button" | "submit"
}) {
  const base = "rounded-xl px-4 py-2 text-sm font-semibold transition"
  const v =
    variant === "primary"
      ? "bg-gradient-to-r from-[#0A5BFF] to-[#00AEEF] text-white hover:brightness-110"
      : variant === "secondary"
        ? "border border-zinc-700 bg-zinc-900 text-zinc-200 hover:bg-zinc-800"
        : "text-zinc-200 hover:bg-zinc-900"

  return (
    <button type={type ?? "button"} disabled={disabled} onClick={onClick} className={clsx(base, v, disabled && "opacity-50", className)}>
      {children}
    </button>
  )
}

