import { PieChart, Pie, Cell, Tooltip, Legend } from 'recharts'

const COLORS = ['#6366f1', '#22d3ee', '#f59e0b', '#10b981']

export default function RegionChart({ byRegion }) {
  return (
    <div style={{ marginBottom: '28px' }}>
      <h3 style={{ margin: '0 0 12px', fontSize: '15px', color: '#374151' }}>
        Revenue by Region
      </h3>
      <PieChart width={340} height={260}>
        <Pie
          data={byRegion}
          dataKey="revenue"
          nameKey="region"
          cx="50%"
          cy="50%"
          innerRadius={70}
          outerRadius={110}
          paddingAngle={3}
        >
          {byRegion.map((_, i) => (
            <Cell key={i} fill={COLORS[i % COLORS.length]} />
          ))}
        </Pie>
        <Tooltip formatter={(v) => v.toLocaleString('en-US', { style: 'currency', currency: 'USD' })} />
        <Legend />
      </PieChart>
    </div>
  )
}
