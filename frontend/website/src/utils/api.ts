function normalizeBaseUrl(baseUrl: string) {
  if (!baseUrl) return ''
  return baseUrl.endsWith('/') ? baseUrl.slice(0, -1) : baseUrl
}

export function apiUrl(path: string) {
  const base = normalizeBaseUrl(String(import.meta.env.VITE_API_BASE_URL || ''))
  if (!path.startsWith('/')) return `${base}/${path}`
  return `${base}${path}`
}

export async function postJson<T>(path: string, body: unknown): Promise<T> {
  const resp = await fetch(apiUrl(path), {
    method: 'POST',
    headers: {
      'content-type': 'application/json',
    },
    body: JSON.stringify(body),
  })

  if (!resp.ok) {
    const text = await resp.text().catch(() => '')
    throw new Error(text || `HTTP ${resp.status}`)
  }

  return (await resp.json()) as T
}

