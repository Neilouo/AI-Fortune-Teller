import { useStore } from '../../hooks/useStore'

export function AgentSelector() {
  const { agents, selectedAgents, toggleAgent } = useStore()

  return (
    <div className="agent-selector">
      <h3>选择大师</h3>
      {agents.map(agent => (
        <div
          key={agent.agent_id}
          className={`agent-toggle ${selectedAgents.includes(agent.agent_id) ? 'active' : ''}`}
          onClick={() => toggleAgent(agent.agent_id)}
          style={{
            borderColor: selectedAgents.includes(agent.agent_id) ? agent.color : undefined,
          }}
        >
          <span className="icon">{agent.icon}</span>
          <span className="name">{agent.display_name}</span>
        </div>
      ))}
    </div>
  )
}
