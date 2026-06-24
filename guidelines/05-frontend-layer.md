# Guideline 05 - Frontend Layer (Session 4)

## Scope
This session owns `frontend/src/` only.

## Setup (run once before writing any component code)
The Vite scaffold is already pre-created - `package.json`, `vite.config.js`, `index.html`, and `src/main.jsx` are all in place. Just install:
```powershell
cd frontend
npm install
```
`frontend/.env` is also pre-created with `VITE_API_URL=http://localhost:8000`. Do not run `npm create vite@latest` - the scaffold already exists and that command would overwrite it.

## What to Build

### App State
`App.jsx` owns all shared state and passes it down via props:
```jsx
const [sessionId, setSessionId] = useState(null)   // set after upload
const [stats, setStats] = useState(null)            // set after /stats fetch
const [loading, setLoading] = useState(false)
const [error, setError] = useState(null)
```

After a successful upload, immediately fetch `/stats/{session_id}` and store the result in `stats`.

### 1. `frontend/src/components/Upload.jsx`
File upload area with a button and drag-and-drop feel.

- `<input type="file" accept=".csv">` - only allow CSV selection
- On file select: POST to `/upload` as multipart form data using `axios`
- Show a loading spinner while uploading
- On success: call `onUploadSuccess(session_id)` prop - App then fetches `/stats`
- On error: display the `detail` field from the API error response
- Disable the input while loading

Props: `onUploadSuccess(sessionId: string)`

### 2. `frontend/src/components/KPICards.jsx`
Row of four cards showing headline numbers.

Cards to show (values come from `stats.kpis`):
| Card | Value |
|---|---|
| Total Revenue | `$125,000.00` - format with `toLocaleString('en-US', {style:'currency',currency:'USD'})` |
| Total Orders | `500` |
| Avg Order Value | `$250.00` |
| Best Month | `2024-03` |
| Best Product | `Widget A` |

Props: `kpis: object`

### 3. `frontend/src/components/Charts.jsx`
Two charts side by side (or stacked on narrow screens).

**Revenue by Month - LineChart (Recharts)**
- Data: `stats.monthly_trend` - `[{month, revenue}]`
- X axis: `month`, Y axis: `revenue`
- Show a `<Tooltip>` and `<CartesianGrid>`

**Top Products - BarChart (Recharts)**
- Data: `stats.top_products` - `[{product, revenue}]`
- X axis: `product`, Y axis: `revenue`

**Anomalies - plain text list below the charts**
- If `stats.anomalies.length > 0`, render a warning box with each anomaly's `month` and `note`
- If empty, render nothing

Props: `stats: object`

### 4. `frontend/src/components/RegionChart.jsx`
Donut (pie) chart showing revenue share by region.

```jsx
import { PieChart, Pie, Cell, Tooltip, Legend } from 'recharts'

const COLORS = ['#6366f1', '#22d3ee', '#f59e0b', '#10b981']

export default function RegionChart({ byRegion }) {
  return (
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
  )
}
```

- Data: `stats.by_region` - `[{region, revenue}]`
- `innerRadius` makes it a donut (ring) rather than a filled pie - easier to read at small sizes
- The four `COLORS` map to the four regions in the sample data

Props: `byRegion: array`

### 5. `frontend/src/components/ChatPanel.jsx`
Chat interface for the AI Q&A feature.

State (local to this component):
```jsx
const [messages, setMessages] = useState([])   // [{role: "user"|"ai", text: string}]
const [input, setInput] = useState("")
const [thinking, setThinking] = useState(false)
```

On submit:
1. Add user message to `messages`
2. POST `{"question": input}` to `/chat/{sessionId}` via axios
3. Add AI response (`answer` field) to `messages`
4. Clear `input`
5. Show a "Thinking..." placeholder while the request is in flight

Props: `sessionId: string`

### 6. `frontend/src/App.jsx`
Layout: renders components in this order:
1. `<Upload>` always visible at top - even after data is loaded (allows re-upload)
2. If `stats` is loaded: `<KPICards kpis={stats.kpis} />`
3. If `stats` is loaded: `<Charts stats={stats} />` (line + bar + anomalies)
4. If `stats` is loaded: `<RegionChart byRegion={stats.by_region} />` (donut)
5. If `sessionId` is set: `<ChatPanel sessionId={sessionId} />`

Show a global error banner if `error` is set.

## API Base URL
All components call axios using the env variable:
```jsx
const API = import.meta.env.VITE_API_URL
axios.post(`${API}/upload`, formData)
axios.get(`${API}/stats/${sessionId}`)
axios.post(`${API}/chat/${sessionId}`, {question})
axios.get(`${API}/export/${sessionId}`, {responseType: 'blob'})
```

## Export Button
Add a simple export button somewhere visible after upload:
```jsx
const handleExport = async () => {
    const res = await axios.get(`${API}/export/${sessionId}`, {responseType: 'blob'})
    const url = URL.createObjectURL(res.data)
    const a = document.createElement('a')
    a.href = url; a.download = 'export.csv'; a.click()
}
```

## Key Constraints
- Backend must be running on `http://localhost:8000` for the app to work
- The chat panel works against the stub response from Session 3 - it will show "AI chat is not yet connected." until Session 5 is done
- No TypeScript - plain JSX throughout
- No CSS frameworks - use inline styles or a single `App.css` file

## Files to Create
- `frontend/src/App.jsx`
- `frontend/src/components/Upload.jsx`
- `frontend/src/components/KPICards.jsx`
- `frontend/src/components/Charts.jsx`
- `frontend/src/components/RegionChart.jsx`
- `frontend/src/components/ChatPanel.jsx`

## Files Already Pre-Created (do not overwrite)
- `frontend/package.json`
- `frontend/vite.config.js`
- `frontend/index.html`
- `frontend/src/main.jsx`
- `frontend/.env`

## Verifying It Works
```powershell
cd frontend
npm run dev
```
Open `http://localhost:5173`, upload `data/sample.csv`, and verify:
- KPI cards appear with correct values
- Line chart shows 6 months of data
- Bar chart shows top products by revenue
- Donut chart shows revenue split across four regions
- Anomaly box appears (April spike in sample data)
- Chat panel appears and can submit a question (stub reply until Session 5)
- Export button downloads a CSV
