import type { BaziRequest, BaziResponse, AgentInfo, ChatRequest, ChatResponse, SSEEvent } from './types'

// 开发环境用 Vite proxy (/api)，生产环境用环境变量指向后端
const BASE = import.meta.env.VITE_API_URL || '/api'

export async function calculateBazi(req: BaziRequest): Promise<BaziResponse> {
  const res = await fetch(`${BASE}/bazi/calculate`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(req),
  })
  if (!res.ok) throw new Error(`Bazi API error: ${res.status}`)
  return res.json()
}

export async function listAgents(): Promise<AgentInfo[]> {
  const res = await fetch(`${BASE}/agents`)
  if (!res.ok) throw new Error(`Agents API error: ${res.status}`)
  return res.json()
}

export async function sendChat(req: ChatRequest): Promise<ChatResponse> {
  const res = await fetch(`${BASE}/chat`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(req),
  })
  if (!res.ok) throw new Error(`Chat API error: ${res.status}`)
  return res.json()
}

export async function createSession(): Promise<{ session_id: string }> {
  const res = await fetch(`${BASE}/session/create`, { method: 'POST' })
  if (!res.ok) throw new Error(`Session API error: ${res.status}`)
  return res.json()
}

export function sendChatStream(
  req: ChatRequest,
  onEvent: (event: SSEEvent) => void,
  onError: (err: Error) => void,
): () => void {
  const controller = new AbortController()

  ;(async () => {
    try {
      const res = await fetch(`${BASE}/chat/stream`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(req),
        signal: controller.signal,
      })
      if (!res.ok || !res.body) {
        throw new Error(`Stream error: ${res.status}`)
      }

      const reader = res.body.getReader()
      const decoder = new TextDecoder()
      let buffer = ''

      while (true) {
        const { done, value } = await reader.read()
        if (done) break
        buffer += decoder.decode(value, { stream: true })

        const lines = buffer.split('\n')
        buffer = lines.pop() || ''

        for (const line of lines) {
          if (line.startsWith('data: ')) {
            try {
              const event = JSON.parse(line.slice(6)) as SSEEvent
              onEvent(event)
            } catch { /* skip malformed */ }
          }
        }
      }
    } catch (err: any) {
      if (err.name !== 'AbortError') {
        onError(err)
      }
    }
  })()

  return () => controller.abort()
}
