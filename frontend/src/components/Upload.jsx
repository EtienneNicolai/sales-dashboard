import { useState } from 'react'
import axios from 'axios'

const API = import.meta.env.VITE_API_URL

export default function Upload({ onUploadSuccess }) {
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const handleChange = async (e) => {
    const file = e.target.files[0]
    if (!file) return

    setLoading(true)
    setError(null)

    const formData = new FormData()
    formData.append('file', file)

    try {
      const res = await axios.post(`${API}/upload`, formData)
      onUploadSuccess(res.data.session_id)
    } catch (err) {
      const detail = err.response?.data?.detail || 'Upload failed. Please try again.'
      setError(detail)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div style={{
      border: '2px dashed #6366f1',
      borderRadius: '12px',
      padding: '32px',
      textAlign: 'center',
      background: '#f8f9ff',
      marginBottom: '24px'
    }}>
      <p style={{ margin: '0 0 16px', color: '#444', fontSize: '16px' }}>
        Upload a CSV file to analyse your sales data
      </p>
      <label style={{
        display: 'inline-block',
        cursor: loading ? 'not-allowed' : 'pointer',
        background: loading ? '#a5b4fc' : '#6366f1',
        color: '#fff',
        padding: '10px 24px',
        borderRadius: '8px',
        fontWeight: '600',
        fontSize: '14px'
      }}>
        {loading ? 'Uploading...' : 'Choose CSV File'}
        <input
          type="file"
          accept=".csv"
          disabled={loading}
          onChange={handleChange}
          style={{ display: 'none' }}
        />
      </label>
      {loading && (
        <p style={{ marginTop: '12px', color: '#6366f1' }}>Processing your file...</p>
      )}
      {error && (
        <p style={{ marginTop: '12px', color: '#dc2626', fontWeight: '500' }}>{error}</p>
      )}
    </div>
  )
}
