export function scoreToLevel(score: number) {
  if (score >= 800) return "A"
  if (score >= 700) return "B"
  if (score >= 600) return "C"
  return "D"
}

