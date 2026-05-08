import { useStore } from '../../hooks/useStore'

const WUXING_COLORS: Record<string, string> = {
  '金': '#FFD700',
  '木': '#4CAF50',
  '水': '#2196F3',
  '火': '#FF5722',
  '土': '#795548',
}

export function BaziSummary() {
  const { baziInfo } = useStore()
  if (!baziInfo) return null

  const maxCount = Math.max(...Object.values(baziInfo.wuxing), 1)
  const pillars = baziInfo.bazi['八字']?.split(' ') || []

  return (
    <div className="bazi-summary">
      <h3>八字信息</h3>
      <div className="bazi-grid">
        {['年柱', '月柱', '日柱', '时柱'].map((label, i) => (
          <div key={label} className="bazi-pillar">
            <div className="label">{label}</div>
            <div className="value">{pillars[i] || '-'}</div>
          </div>
        ))}
      </div>
      <div style={{ fontSize: 12, color: 'var(--text-secondary)', marginBottom: 8 }}>
        {baziInfo.zodiac}年 · {baziInfo.constellation}
      </div>
      <div className="wuxing-bar">
        {Object.entries(baziInfo.wuxing).map(([name, count]) => (
          <div key={name} className="wuxing-item">
            <div className="name">{name}</div>
            <div className="bar">
              <div
                className="bar-fill"
                style={{
                  width: `${(count / maxCount) * 100}%`,
                  background: WUXING_COLORS[name] || '#888',
                }}
              />
            </div>
            <div className="count">{count}</div>
          </div>
        ))}
      </div>
    </div>
  )
}
