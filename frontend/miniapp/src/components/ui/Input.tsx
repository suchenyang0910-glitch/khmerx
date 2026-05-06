import type { InputHTMLAttributes } from "react"
import { cn } from "@/lib/utils"

export default function Input({ className, ...props }: InputHTMLAttributes<HTMLInputElement>) {
  return (
    <input
      className={cn(
        "h-12 w-full rounded-xl border border-zinc-200 bg-white px-3 text-sm outline-none focus:ring-2 focus:ring-blue-200",
        className,
      )}
      {...props}
    />
  )
}

