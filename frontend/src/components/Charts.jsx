import {
  LineChart,
  Line,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer
} from 'recharts'

export default function Charts({ stats }) {
  const { monthly_trend, top_products, anomalies } = stats

  return (
    <div style={{ marginBottom: '28px' }}>
      <div style={{ display: 'flex', gap: '24px', flexWrap: 'wrap' }}>
        {/* Revenue by Month */}
        <div style={{ flex: '1 1 320px', minWidth: '280px' }}>
          <h3 style={{ margin: '0 0 12px', fontSize: '15px', color: '#374151' }}>
            Revenue by Month
          </h3>
          <ResponsiveContainer width="100%" height={240}>
            <LineChart data={monthly_trend}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="month" tick={{ fontSize: 12 }} />
              <YAxis tick={{ fontSize: 12 }} />
              <Tooltip
                formatter={(v) =>
                  v.toLocaleString('en-US', { style: 'currency', currency: 'USD' })
                }
              />
              <Line type="monotone" dataKey="revenue" stroke="#6366f1" strokeWidth={2} dot={false} />
            </LineChart>
          </ResponsiveContainer>
        </div>

        {/* Top Products */}
        <div style={{ flex: '1 1 320px', minWidth: '280px' }}>
          <h3 style={{ margin: '0 0 12px', fontSize: '15px', color: '#374151' }}>
            Top Products by Revenue
          </h3>
          <ResponsiveContainer width="100%" height={240}>
            <BarChart data={top_products}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="product" tick={{ fontSize: 12 }} />
              <YAxis tick={{ fontSize: 12 }} />
              <Tooltip
                formatter={(v) =>
                  v.toLocaleString('en-US', { style: 'currency', currency: 'USD' })
                }
              />
              <Bar dataKey="revenue" fill="#22d3ee" radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Anomalies */}
      {anomalies && anomalies.length > 0 && (
        <div style={{
          marginTop: '20px',
          background: '#fef9c3',
          border: '1px solid #fde68a',
          borderRadius: '10px',
          padding: '16px 20px'
        }}>
          <strong style={{ color: '#92400e', fontSize: '14px' }}>
            Anomalies Detected
          </strong>
          <ul style={{ margin: '8px 0 0', padding: '0 0 0 18px' }}>
            {anomalies.map((a, i) => (
              <li key={i} style={{ color: '#78350f', fontSize: '14px', marginBottom: '4px' }}>
                <strong>{a.month}</strong> — {a.note}
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  )
}
