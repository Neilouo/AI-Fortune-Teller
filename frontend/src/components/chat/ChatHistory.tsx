import { useEffect, useRef } from 'react'
import { useStore } from '../../hooks/useStore'
import { ResponseGrid } from './ResponseGrid'

export function ChatHistory() {
  const { chatHistory, isLoading, streamingResponses } = useStore()
  const endRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    endRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [chatHistory, streamingResponses])

  const streamingList = Object.values(streamingResponses)

  return (
    <div className="chat-history">
      {chatHistory.map(msg => (
        <div key={msg.id}>
          {msg.role === 'user' && (
            <div className="user-message">{msg.content}</div>
          )}
          {msg.role === 'responses' && msg.responses && (
            <ResponseGrid responses={msg.responses} />
          )}
        </div>
      ))}

      {isLoading && streamingList.length > 0 && (
        <ResponseGrid responses={streamingList} loading />
      )}

      {isLoading && streamingList.length === 0 && (
        <div style={{ color: 'var(--text-muted)', fontSize: 13, padding: '8px 0' }}>
          大师们正在思考中...
        </div>
      )}

      <div ref={endRef} />
    </div>
  )
}
