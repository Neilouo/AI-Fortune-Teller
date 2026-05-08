import { create } from 'zustand'
import type { AgentInfo, BaziResponse, ChatMessage, AgentResponse } from '../api/types'
import * as api from '../api/client'

interface AppState {
  // Session
  sessionId: string | null

  // BaZi
  baziInfo: BaziResponse | null
  baziLoading: boolean

  // Agents
  agents: AgentInfo[]
  selectedAgents: string[]

  // Chat
  chatHistory: ChatMessage[]
  isLoading: boolean
  streamingResponses: Record<string, AgentResponse>

  // Step tracking
  step: 'birth' | 'chat'

  // Actions
  init: () => Promise<void>
  setBirthInfo: (year: number, month: number, day: number, hour: number) => Promise<void>
  toggleAgent: (agentId: string) => void
  sendMessage: (message: string) => void
  resetSession: () => void
  goToChat: () => void
}

let idCounter = 0
const genId = () => `msg_${++idCounter}_${Date.now()}`

export const useStore = create<AppState>((set, get) => ({
  sessionId: null,
  baziInfo: null,
  baziLoading: false,
  agents: [],
  selectedAgents: [],
  chatHistory: [],
  isLoading: false,
  streamingResponses: {},
  step: 'birth',

  init: async () => {
    try {
      const agents = await api.listAgents()
      const session = await api.createSession()
      set({
        agents,
        selectedAgents: agents.map(a => a.agent_id),
        sessionId: session.session_id,
      })
    } catch (err) {
      console.error('Init failed:', err)
    }
  },

  setBirthInfo: async (year, month, day, hour) => {
    set({ baziLoading: true })
    try {
      const info = await api.calculateBazi({ year, month, day, hour })
      set({ baziInfo: info, baziLoading: false, step: 'chat' })
    } catch (err) {
      console.error('BaZi calculation failed:', err)
      set({ baziLoading: false })
    }
  },

  toggleAgent: (agentId) => {
    const { selectedAgents } = get()
    if (selectedAgents.includes(agentId)) {
      if (selectedAgents.length > 1) {
        set({ selectedAgents: selectedAgents.filter(id => id !== agentId) })
      }
    } else {
      set({ selectedAgents: [...selectedAgents, agentId] })
    }
  },

  sendMessage: (message) => {
    const { sessionId, selectedAgents, chatHistory } = get()
    if (!sessionId || !message.trim()) return

    // Add user message
    const userMsg: ChatMessage = {
      id: genId(),
      role: 'user',
      content: message,
      timestamp: Date.now(),
    }
    set({ chatHistory: [...chatHistory, userMsg], isLoading: true, streamingResponses: {} })

    // Use SSE stream
    api.sendChatStream(
      { session_id: sessionId, message, selected_agents: selectedAgents },
      (event) => {
        if (event.type === 'response') {
          set(state => ({
            streamingResponses: {
              ...state.streamingResponses,
              [event.data.agent_id]: event.data,
            },
          }))
        } else if (event.type === 'done') {
          const { streamingResponses, chatHistory: history } = get()
          const responses = Object.values(streamingResponses)
          const responseMsg: ChatMessage = {
            id: genId(),
            role: 'responses',
            responses,
            emotion: '',
            topic: '',
            timestamp: Date.now(),
          }
          set({
            chatHistory: [...history, responseMsg],
            isLoading: false,
            streamingResponses: {},
          })
        }
      },
      (err) => {
        console.error('Stream error:', err)
        set({ isLoading: false })
      },
    )
  },

  resetSession: () => {
    set({
      baziInfo: null,
      chatHistory: [],
      step: 'birth',
      isLoading: false,
      streamingResponses: {},
    })
  },

  goToChat: () => set({ step: 'chat' }),
}))
