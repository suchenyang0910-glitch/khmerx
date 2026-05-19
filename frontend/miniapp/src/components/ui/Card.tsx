import type { HTMLAttributes } from "react"
import { cn } from "@/lib/utils"

export default function Card({ className, ...props }: HTMLAttributes<HTMLDivElement>) {
  return (
    <div
      className={cn(
        "rounded-2xl bg-white shadow-sm border border-zinc-100",
        className,
      )}
      {...props}
    />
  )
}

