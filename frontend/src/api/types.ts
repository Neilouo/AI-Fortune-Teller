export interface BaziRequest {
  year: number
  month: number
  day: number
  hour: number
}

export interface BaziResponse {
  bazi: Record<string, string>
  wuxing: Record<string, number>
  strongest: string
  weakest: string
  zodiac: string
  constellation: string
  personality_traits: string[]
}

export interface AgentInfo {
  agent_id: string
  display_name: string
  icon: string
  color: string
  description: string
}

export interface AgentResponse {
  agent_id: string
  display_name: string
  icon: string
  content: string
  error: string | null
}

export interface ChatRequest {
  session_id: string
  message: string
  selected_agents: string[]
}

export interface ChatResponse {
  user_message: string
  emotion: string
  emotion_intensity: number
  topic: string
  responses: AgentResponse[]
}

export interface ChatMessage {
  id: string
  role: 'user' | 'responses'
  content?: string
  responses?: AgentResponse[]
  emotion?: string
  topic?: string
  timestamp: number
}

export interface SSEMeta {
  type: 'meta'
  user_message: string
  emotion: string
  emotion_intensity: number
  topic: string
}

export interface SSEResponse {
  type: 'response'
  data: AgentResponse
}

export interface SSEDone {
  type: 'done'
}

export type SSEEvent = SSEMeta | SSEResponse | SSEDone
