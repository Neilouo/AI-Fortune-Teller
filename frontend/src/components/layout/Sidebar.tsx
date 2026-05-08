import { useStore } from '../../hooks/useStore'
import { AgentSelector } from '../agents/AgentSelector'
import { BaziSummary } from '../onboarding/BaziSummary'

export function Sidebar() {
  const { baziInfo, step, resetSession } = useStore()

  return (
    <div className="sidebar">
      <div>
        <h2 style={{ fontSize: 18, marginBottom: 4 }}>🔮 算命大师</h2>
        <p style={{ fontSize: 12, color: 'var(--text-muted)' }}>多宗教 AI 智慧</p>
      </div>

      {step === 'chat' && (
        <>
          {baziInfo && <BaziSummary />}
          <AgentSelector />
          <button className="sidebar-btn" onClick={resetSession}>
            重新开始
          </button>
        </>
      )}
    </div>
  )
}
