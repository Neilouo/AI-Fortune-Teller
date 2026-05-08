import { useStore } from '../../hooks/useStore'
import { ChatHistory } from './ChatHistory'
import { ChatInput } from './ChatInput'
import { SuggestedQuestions } from './SuggestedQuestions'

export function ChatArea() {
  const { chatHistory } = useStore()

  return (
    <div className="chat-area">
      <ChatHistory />
      {chatHistory.length === 0 && <SuggestedQuestions />}
      <ChatInput />
    </div>
  )
}
