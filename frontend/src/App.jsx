import { useState } from 'react'
import axios from 'axios'
import Upload from './components/Upload'
import KPICards from './components/KPICards'
import Charts from './components/Charts'
import RegionChart from './components/RegionChart'
import ChatPanel from './components/ChatPanel'

const API = import.meta.env.VITE_API_URL

export default function App() {
  const [sessionId, setSessionId] = useState(null)
  const [stats, setStats] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const handleUploadSuccess = async (id) => {
    setSessionId(id)
    setStats(null)
    setError(null)
    setLoading(true)
    try {
      const res = await axios.get(`${API}/stats/${id}`)
      setStats(res.data)
    } catch (err) {
      const detail = err.response?.data?.detail || 'Failed to load stats.'
      setError(detail)
    } finally {
      setLoading(false)
    }
  }

  const handleExport = async () => {
    try {
      const res = await axios.get(`${API}/export/${sessionId}`, { responseType: 'blob' })
      const url = URL.createObjectURL(res.data)
      const a = document.createElement('a')
      a.href = url
      a.download = 'export.csv'
      a.click()
      URL.revokeObjectURL(url)
    } catch (err) {
      setError('Export failed.')
    }
  }

  return (
    <div style={{
      maxWidth: '960px',
      margin: '0 auto',
      padding: '32px 20px',
      fontFamily: "'Segoe UI', system-ui, sans-serif",
      color: '#111827'
    }}>
      <h1 style={{ margin: '0 0 8px', fontSize: '28px', fontWeight: '700', color: '#1e293b' }}>
        Sales Dashboard
      </h1>
      <p style={{ margin: '0 0 28px', color: '#6b7280', fontSize: '15px' }}>
        Upload a CSV to analyse your sales data, explore charts, and ask questions.
      </p>

      {error && (
        <div style={{
          background: '#fef2f2',
          border: '1px solid #fecaca',
          borderRadius: '10px',
          padding: '14px 18px',
          marginBottom: '20px',
          color: '#dc2626',
          fontSize: '14px'
        }}>
          {error}
        </div>
      )}

      <Upload onUploadSuccess={handleUploadSuccess} />

      {loading && (
        <p style={{ color: '#6366f1', fontWeight: '500' }}>Loading analysis...</p>
      )}

      {stats && sessionId && (
        <div style={{ marginTop: '4px' }}>
          <div style={{ display: 'flex', justifyContent: 'flex-end', marginBottom: '16px' }}>
            <button
              onClick={handleExport}
              style={{
                background: '#10b981',
                color: '#fff',
                border: 'none',
                borderRadius: '8px',
                padding: '9px 20px',
                fontWeight: '600',
                fontSize: '14px',
                cursor: 'pointer'
              }}
            >
              Export CSV
            </button>
          </div>

          <KPICards kpis={stats.kpis} />
          <Charts stats={stats} />
          <RegionChart byRegion={stats.by_region} />
        </div>
      )}

      {sessionId && (
        <ChatPanel sessionId={sessionId} />
      )}
    </div>
  )
}
