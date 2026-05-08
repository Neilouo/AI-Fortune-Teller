import { useStore } from '../../hooks/useStore'

export function Header() {
  const { baziInfo, step } = useStore()

  return (
    <div className="header">
      <h1>AI 算命大师</h1>
      <p>
        {step === 'birth'
          ? '输入您的生辰信息，开启多宗教智慧之旅'
          : baziInfo
            ? `${baziInfo.zodiac}年 · ${baziInfo.constellation} · 五行最强: ${baziInfo.strongest}`
            : '多宗教 AI 算命'}
      </p>
    </div>
  )
}
