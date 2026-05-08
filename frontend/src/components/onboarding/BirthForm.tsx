import { useState } from 'react'
import { useStore } from '../../hooks/useStore'

export function BirthForm() {
  const { setBirthInfo, baziLoading } = useStore()
  const [year, setYear] = useState(1990)
  const [month, setMonth] = useState(1)
  const [day, setDay] = useState(1)
  const [hour, setHour] = useState(12)

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    setBirthInfo(year, month, day, hour)
  }

  return (
    <div className="birth-form">
      <h2>请输入您的生辰信息</h2>
      <form onSubmit={handleSubmit}>
        <div className="form-row">
          <div className="form-group">
            <label>出生年份</label>
            <input
              type="number"
              min={1900}
              max={2030}
              value={year}
              onChange={e => setYear(+e.target.value)}
            />
          </div>
          <div className="form-group">
            <label>出生月份</label>
            <select value={month} onChange={e => setMonth(+e.target.value)}>
              {Array.from({ length: 12 }, (_, i) => (
                <option key={i + 1} value={i + 1}>{i + 1}月</option>
              ))}
            </select>
          </div>
        </div>
        <div className="form-row">
          <div className="form-group">
            <label>出生日期</label>
            <select value={day} onChange={e => setDay(+e.target.value)}>
              {Array.from({ length: 31 }, (_, i) => (
                <option key={i + 1} value={i + 1}>{i + 1}日</option>
              ))}
            </select>
          </div>
          <div className="form-group">
            <label>出生时辰 (0-23时)</label>
            <input
              type="range"
              min={0}
              max={23}
              value={hour}
              onChange={e => setHour(+e.target.value)}
              style={{ marginTop: 8 }}
            />
            <div style={{ textAlign: 'center', fontSize: 13, color: 'var(--text-secondary)' }}>
              {hour}:00 ({getChineseHour(hour)})
            </div>
          </div>
        </div>
        <button type="submit" className="btn btn-primary" disabled={baziLoading}>
          {baziLoading ? '计算中...' : '开始算命'}
        </button>
      </form>
    </div>
  )
}

function getChineseHour(hour: number): string {
  const periods = [
    '子时', '子时', '丑时', '丑时', '寅时', '寅时',
    '卯时', '卯时', '辰时', '辰时', '巳时', '巳时',
    '午时', '午时', '未时', '未时', '申时', '申时',
    '酉时', '酉时', '戌时', '戌时', '亥时', '亥时',
  ]
  return periods[hour]
}
