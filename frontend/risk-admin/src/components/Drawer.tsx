import { X } from 'lucide-react'
import { cn } from '@/lib/utils'

export default function Drawer(props: {
  open: boolean
  title: string
  onClose: () => void
  children: React.ReactNode
  widthClassName?: string
}) {
  if (!props.open) return null

  return (
    <div className="fixed inset-0 z-50">
      <div className="absolute inset-0 bg-black/30" onClick={props.onClose} />
      <div
        className={cn(
          'absolute right-0 top-0 h-full w-full max-w-2xl border-l border-zinc-200 bg-white shadow-xl',
          props.widthClassName
        )}
      >
        <div className="flex h-14 items-center justify-between border-b border-zinc-200 px-4">
          <div className="min-w-0 truncate text-sm font-semibold text-zinc-900">{props.title}</div>
          <button
            type="button"
            onClick={props.onClose}
            className="inline-flex h-9 w-9 items-center justify-center rounded-lg border border-zinc-200 bg-white text-zinc-700 transition hover:bg-zinc-50"
          >
            <X className="h-4 w-4" />
          </button>
        </div>
        <div className="h-[calc(100%-56px)] overflow-auto p-4">{props.children}</div>
      </div>
    </div>
  )
}

