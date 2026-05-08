import { useState, type KeyboardEvent } from 'react'
import { useStore } from '../../hooks/useStore'

export function ChatInput() {
  const { sendMessage, isLoading } = useStore()
  const [input, setInput] = useState('')

  const handleSend = () => {
    if (!input.trim() || isLoading) return
    sendMessage(input.trim())
    setInput('')
  }

  const handleKeyDown = (e: KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSend()
    }
  }

  return (
    <div className="chat-input-area">
      <div className="chat-input-wrapper">
        <input
          className="chat-input"
          placeholder="向大师们提问... (Enter 发送)"
          value={input}
          onChange={e => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          disabled={isLoading}
        />
        <button
          className="send-btn"
          onClick={handleSend}
          disabled={isLoading || !input.trim()}
        >
          发送
        </button>
      </div>
    </div>
  )
}
