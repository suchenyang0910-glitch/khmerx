import clsx from "clsx"

export function Card({
  className,
  children,
}: {
  className?: string
  children: React.ReactNode
}) {
  return <div className={clsx("rounded-2xl border border-zinc-800 bg-zinc-900/40 p-5", className)}>{children}</div>
}

