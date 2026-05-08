import { useStore } from '../../hooks/useStore'

const QUESTION_GROUPS = [
  {
    label: '事业财运',
    questions: ['我的事业运势如何？', '最近适合投资理财吗？', '我适合创业吗？'],
  },
  {
    label: '感情姻缘',
    questions: ['我的桃花运怎么样？', '我和另一半的关系如何发展？', '什么时候能遇到对的人？'],
  },
  {
    label: '健康运势',
    questions: ['最近身体健康需要注意什么？', '我的整体运势如何？'],
  },
]

export function SuggestedQuestions() {
  const { sendMessage, isLoading } = useStore()

  return (
    <div style={{ padding: '0 32px 16px' }}>
      {QUESTION_GROUPS.map(group => (
        <div key={group.label} className="suggested-questions">
          <h4>{group.label}</h4>
          {group.questions.map(q => (
            <button
              key={q}
              className="question-chip"
              onClick={() => !isLoading && sendMessage(q)}
              disabled={isLoading}
            >
              {q}
            </button>
          ))}
        </div>
      ))}
    </div>
  )
}
