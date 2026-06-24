const cardStyle = {
  background: '#fff',
  border: '1px solid #e5e7eb',
  borderRadius: '12px',
  padding: '20px 24px',
  flex: '1 1 160px',
  minWidth: '140px',
  boxShadow: '0 1px 4px rgba(0,0,0,0.06)'
}

const labelStyle = {
  fontSize: '12px',
  fontWeight: '600',
  color: '#6b7280',
  textTransform: 'uppercase',
  letterSpacing: '0.05em',
  marginBottom: '6px'
}

const valueStyle = {
  fontSize: '22px',
  fontWeight: '700',
  color: '#111827'
}

function Card({ label, value }) {
  return (
    <div style={cardStyle}>
      <div style={labelStyle}>{label}</div>
      <div style={valueStyle}>{value}</div>
    </div>
  )
}

export default function KPICards({ kpis }) {
  const fmt = (n) =>
    n.toLocaleString('en-US', { style: 'currency', currency: 'USD' })

  return (
    <div style={{ display: 'flex', gap: '16px', flexWrap: 'wrap', marginBottom: '28px' }}>
      <Card label="Total Revenue" value={fmt(kpis.total_revenue)} />
      <Card label="Total Orders" value={kpis.total_orders.toLocaleString()} />
      <Card label="Avg Order Value" value={fmt(kpis.avg_order_value)} />
      <Card label="Best Month" value={kpis.best_month} />
      <Card label="Best Product" value={kpis.best_product} />
    </div>
  )
}
