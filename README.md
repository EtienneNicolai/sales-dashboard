# Sales Dashboard

A full-stack web app that ingests a CSV of sales data, runs automated analysis, and lets you ask plain-English questions about the data using AI.

## Features

- CSV upload and validation
- KPI cards — total revenue, total orders, average order value, best month, best product
- Line chart — revenue trend over time
- Bar chart — top products by revenue
- Donut chart — revenue split by region
- Anomaly detection — flags unusual months automatically
- AI chat — ask plain-English questions about your data
- CSV export

## Requirements

### API Key
This project requires a **paid Google AI Studio API key**.

1. Go to [aistudio.google.com](https://aistudio.google.com)
2. Sign in and enable billing on your account
3. Create an API key
4. Add it to your `.env` file (see setup below)

The free tier has quota limits that prevent the chat feature from working. A paid key is required.

### Software
- Python 3.11+
- Node.js 18+

## Setup

**1. Clone the repo**
```
git clone https://github.com/EtienneNicolai/sales-dashboard.git
cd sales-dashboard
```

**2. Install backend packages**
```
python -m pip install --target=backend\lib -r requirements.txt
```

**3. Install frontend packages**
```
cd frontend
npm install
cd ..
```

**4. Create your `.env` file**
```
copy .env.example .env
```
Open `.env` and replace `your-gemini-key-here` with your real API key.

**5. Start the app**

Double-click `start.bat` — opens the backend and frontend in separate windows automatically.

Then open [http://localhost:5173](http://localhost:5173) in your browser.

## CSV Format

Your CSV must contain exactly these seven columns:

| Column | Type | Example |
|---|---|---|
| `date` | Date (YYYY-MM-DD) | `2024-01-15` |
| `product` | Text | `Widget A` |
| `category` | Text | `Electronics` |
| `quantity` | Integer | `10` |
| `unit_price` | Decimal | `29.99` |
| `revenue` | Decimal | `299.90` |
| `region` | Text | `North` |

Column names must match exactly (case-sensitive). Rows where `revenue` is zero or missing are ignored.

A sample file is included at `data/sample.csv` — use it to try the app before uploading your own data.

## Architecture

```
sales-dashboard/
├── backend/
│   └── src/
│       ├── data/        # CSV parsing and data model
│       ├── analysis/    # KPIs, trends, anomaly detection
│       ├── api/         # FastAPI routes
│       └── ai/          # Gemini API chat integration
├── frontend/
│   └── src/
│       └── components/  # React UI components
└── data/
    └── sample.csv       # Example dataset
```

**Backend:** FastAPI + Pandas + Google Generative AI  
**Frontend:** React + Vite + Recharts
