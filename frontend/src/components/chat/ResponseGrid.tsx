import type { AgentResponse } from '../../api/types'
import { useStore } from '../../hooks/useStore'

interface Props {
  responses: AgentResponse[]
  loading?: boolean
}

export function ResponseGrid({ responses, loading }: Props) {
  const { agents } = useStore()

  const getAgentColor = (agentId: string) =>
    agents.find(a => a.agent_id === agentId)?.color || '#888'

  return (
    <div className="response-grid">
      {responses.map(resp => (
        <div
          key={resp.agent_id}
          className={`response-card ${loading && !resp.content ? 'loading' : ''}`}
          style={{ borderLeftColor: getAgentColor(resp.agent_id), borderLeftWidth: 3 }}
        >
          <div className="card-header">
            <span className="card-icon">{resp.icon}</span>
            <span className="card-name">{resp.display_name}</span>
          </div>
          {resp.error ? (
            <div className="card-error">出错了: {resp.error}</div>
          ) : (
            <div className="card-content">{resp.content || ''}</div>
          )}
        </div>
      ))}
    </div>
  )
}
