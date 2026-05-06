export function fmtCountdown(deadlineIso?: string | null) {
  if (!deadlineIso) return null
  const ms = new Date(deadlineIso).getTime() - Date.now()
  if (Number.isNaN(ms)) return null
  if (ms <= 0) return "00:00:00"
  const s = Math.floor(ms / 1000)
  const hh = String(Math.floor(s / 3600)).padStart(2, "0")
  const mm = String(Math.floor((s % 3600) / 60)).padStart(2, "0")
  const ss = String(s % 60).padStart(2, "0")
  return `${hh}:${mm}:${ss}`
}

export function stepIndex(status: string) {
  if (status === "matched") return 1
  if (status === "lend_confirmed") return 2
  if (status === "repayment_confirmed") return 3
  if (status === "repaying") return 4
  if (status === "completed") return 5
  return 0
}

