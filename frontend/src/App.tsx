import { useEffect } from 'react'
import { useStore } from './hooks/useStore'
import { Header } from './components/layout/Header'
import { Sidebar } from './components/layout/Sidebar'
import { BirthForm } from './components/onboarding/BirthForm'
import { ChatArea } from './components/chat/ChatArea'

export default function App() {
  const { step, init } = useStore()

  useEffect(() => {
    init()
  }, [init])

  return (
    <div className="app-container">
      <Sidebar />
      <div className="main-content">
        <Header />
        {step === 'birth' ? <BirthForm /> : <ChatArea />}
      </div>
    </div>
  )
}
