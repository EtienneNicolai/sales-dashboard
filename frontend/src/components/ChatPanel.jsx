import { useState } from 'react'
import axios from 'axios'

const API = import.meta.env.VITE_API_URL

export default function ChatPanel({ sessionId }) {
  const [messages, setMessages] = useState([])
  const [input, setInput] = useState('')
  const [thinking, setThinking] = useState(false)

  const handleSubmit = async (e) => {
    e.preventDefault()
    const question = input.trim()
    if (!question || thinking) return

    setMessages((prev) => [...prev, { role: 'user', text: question }])
    setInput('')
    setThinking(true)

    try {
      const res = await axios.post(`${API}/chat/${sessionId}`, { question })
      setMessages((prev) => [...prev, { role: 'ai', text: res.data.answer }])
    } catch (err) {
      const detail = err.response?.data?.detail || 'Something went wrong.'
      setMessages((prev) => [...prev, { role: 'ai', text: `Error: ${detail}` }])
    } finally {
      setThinking(false)
    }
  }

  return (
    <div style={{
      border: '1px solid #e5e7eb',
      borderRadius: '12px',
      background: '#fff',
      overflow: 'hidden',
      marginBottom: '24px'
    }}>
      <div style={{
        background: '#6366f1',
        padding: '12px 20px',
        color: '#fff',
        fontWeight: '600',
        fontSize: '15px'
      }}>
        Ask a question about your data
      </div>

      <div style={{
        minHeight: '160px',
        maxHeight: '320px',
        overflowY: 'auto',
        padding: '16px 20px',
        display: 'flex',
        flexDirection: 'column',
        gap: '12px'
      }}>
        {messages.length === 0 && (
          <p style={{ color: '#9ca3af', fontSize: '14px', margin: 0 }}>
            Ask anything about your sales data — e.g. "Which product had the worst Q2?"
          </p>
        )}
        {messages.map((msg, i) => (
          <div key={i} style={{
            alignSelf: msg.role === 'user' ? 'flex-end' : 'flex-start',
            background: msg.role === 'user' ? '#6366f1' : '#f3f4f6',
            color: msg.role === 'user' ? '#fff' : '#111827',
            padding: '10px 14px',
            borderRadius: msg.role === 'user' ? '12px 12px 2px 12px' : '12px 12px 12px 2px',
            maxWidth: '75%',
            fontSize: '14px',
            lineHeight: '1.5'
          }}>
            {msg.text}
          </div>
        ))}
        {thinking && (
          <div style={{
            alignSelf: 'flex-start',
            background: '#f3f4f6',
            color: '#6b7280',
            padding: '10px 14px',
            borderRadius: '12px 12px 12px 2px',
            fontSize: '14px',
            fontStyle: 'italic'
          }}>
            Thinking...
          </div>
        )}
      </div>

      <form onSubmit={handleSubmit} style={{
        display: 'flex',
        borderTop: '1px solid #e5e7eb',
        padding: '12px 16px',
        gap: '8px'
      }}>
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Type your question..."
          disabled={thinking}
          style={{
            flex: 1,
            border: '1px solid #d1d5db',
            borderRadius: '8px',
            padding: '9px 14px',
            fontSize: '14px',
            outline: 'none'
          }}
        />
        <button
          type="submit"
          disabled={thinking || !input.trim()}
          style={{
            background: thinking || !input.trim() ? '#a5b4fc' : '#6366f1',
            color: '#fff',
            border: 'none',
            borderRadius: '8px',
            padding: '9px 20px',
            fontWeight: '600',
            fontSize: '14px',
            cursor: thinking || !input.trim() ? 'not-allowed' : 'pointer'
          }}
        >
          Send
        </button>
      </form>
    </div>
  )
}
