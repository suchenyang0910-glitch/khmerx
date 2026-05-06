import { useMemo } from "react"

type Props = {
  values: number[]
  stroke?: string
}

export default function Sparkline({ values, stroke = "#3b82f6" }: Props) {
  const points = useMemo(() => {
    if (!values.length) return ""
    const w = 120
    const h = 36
    const max = Math.max(...values)
    const min = Math.min(...values)
    const span = Math.max(1, max - min)
    return values
      .map((v, i) => {
        const x = (i / Math.max(1, values.length - 1)) * w
        const y = h - ((v - min) / span) * h
        return `${x.toFixed(2)},${y.toFixed(2)}`
      })
      .join(" ")
  }, [values])

  return (
    <svg width={120} height={36} viewBox="0 0 120 36" aria-hidden="true">
      <polyline fill="none" stroke={stroke} strokeWidth={2} strokeLinejoin="round" strokeLinecap="round" points={points} />
    </svg>
  )
}

