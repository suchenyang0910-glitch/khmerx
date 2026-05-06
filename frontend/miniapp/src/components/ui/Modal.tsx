import type { ReactNode } from "react"
import { cn } from "@/lib/utils"

export default function Modal({
  open,
  title,
  children,
  onClose,
}: {
  open: boolean
  title?: string
  children: ReactNode
  onClose: () => void
}) {
  if (!open) return null

  return (
    <div className="fixed inset-0 z-50">
      <button
        className="absolute inset-0 bg-black/40"
        onClick={onClose}
        aria-label="close"
      />
      <div className="absolute inset-x-0 bottom-0 mx-auto w-full max-w-md">
        <div className={cn("rounded-t-3xl bg-white p-4 shadow-xl")}> 
          {title ? (
            <div className="mb-3 text-sm font-semibold text-zinc-900">{title}</div>
          ) : null}
          {children}
        </div>
      </div>
    </div>
  )
}

