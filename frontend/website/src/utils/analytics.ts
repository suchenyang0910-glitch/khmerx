type TrackProps = Record<string, unknown>

export function track(event: string, props: TrackProps = {}) {
  const payload = { event, ...props, ts: Date.now() }
  const w = window as unknown as { dataLayer?: unknown[] }
  if (Array.isArray(w.dataLayer)) w.dataLayer.push(payload)
  if (import.meta.env.DEV) {
    console.debug('[track]', payload)
  }
}
