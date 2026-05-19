import { cn } from "@/lib/utils"

export default function Segmented<T extends string>({
  value,
  options,
  onChange,
}: {
  value: T
  options: Array<{ value: T; label: string }>
  onChange: (v: T) => void
}) {
  return (
    <div className="grid grid-cols-3 gap-2 rounded-2xl bg-zinc-100 p-1">
      {options.map((o) => (
        <button
          key={o.value}
          onClick={() => onChange(o.value)}
          className={cn(
            "h-10 rounded-xl text-sm font-medium transition-colors",
            o.value === value
              ? "bg-white text-zinc-900 shadow-sm"
              : "text-zinc-600 hover:bg-white/70",
          )}
        >
          {o.label}
        </button>
      ))}
    </div>
  )
}

