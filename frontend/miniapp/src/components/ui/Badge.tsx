import type { HTMLAttributes } from "react"
import { cn } from "@/lib/utils"

type Props = HTMLAttributes<HTMLSpanElement> & {
  tone?: "blue" | "green" | "yellow" | "red" | "zinc"
}

export default function Badge({ className, tone = "zinc", ...props }: Props) {
  return (
    <span
      className={cn(
        "inline-flex items-center rounded-full px-2 py-0.5 text-xs font-medium",
        tone === "zinc" && "bg-zinc-100 text-zinc-700",
        tone === "blue" && "bg-blue-50 text-blue-700",
        tone === "green" && "bg-green-50 text-green-700",
        tone === "yellow" && "bg-amber-50 text-amber-700",
        tone === "red" && "bg-red-50 text-red-700",
        className,
      )}
      {...props}
    />
  )
}

