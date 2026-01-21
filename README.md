# InsightCast

<p align="center">
  <img src="https://img.shields.io/badge/status-active-success.svg" alt="Status">
  <img src="https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white" alt="FastAPI">
  <img src="https://img.shields.io/badge/React-61DAFB?logo=react&logoColor=black" alt="React">
  <img src="https://img.shields.io/badge/TypeScript-3178C6?logo=typescript&logoColor=white" alt="TypeScript">
  <img src="https://img.shields.io/badge/Vite-646CFF?logo=vite&logoColor=white" alt="Vite">
  <br>
  <img src="https://img.shields.io/badge/Pandas-150458?logo=pandas&logoColor=white" alt="Pandas">
  <img src="https://img.shields.io/badge/Recharts-FF6384?logo=chartdotjs&logoColor=white" alt="Recharts">
  <img src="https://img.shields.io/badge/Framer-0055FF?logo=framer&logoColor=white" alt="Framer Motion">
  <img src="https://img.shields.io/badge/Prophet-4285F4?logo=meta&logoColor=white" alt="Prophet">
</p>

A time-series forecasting platform that predicts future trends and catches unusual patterns in your data. Upload your CSV, get instant predictions, and spot problems before they happen.

---

## Screenshots

### Interactive Anomaly Detection
![Forecast Chart](assets/screenshot-chart.png)
*Zoom into any time range and see anomalies update in real-time*

### Dashboard
![Dashboard](assets/screenshot-dashboard.png)
*Everything you need: model stats, insights, and recommended actions*

### Getting Started
![Empty State](assets/screenshot-empty-state.png)
*Clean interface with sample data to try it out*

---

## How It Works

**Backend:** FastAPI server running Meta's Prophet library for forecasting. Detects anomalies, calculates metrics, and generates PDF reports.

**Frontend:** React app with interactive charts (Recharts) and smooth animations (Framer Motion). Everything updates in real-time.

**Stack:**
- Prophet for time-series forecasting
- FastAPI + Uvicorn for the API
- React 19 + TypeScript + Vite
- ReportLab for PDF generation

---

## Features

- Forecast future trends with Prophet (handles seasonality automatically)
- Detect anomalies and categorize by severity (High/Medium/Low)
- Get plain-English insights instead of just numbers
- Download professional PDF reports
- Interactive chart with zoom/brush controls
- Switch between additive/multiplicative seasonality modes

---

## Installation

### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: .\venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

Open `http://localhost:5173` in your browser.

---

## Usage

1. Upload a CSV with `ds` (date) and `y` (value) columns
2. Set your forecast horizon and seasonality mode
3. Click "Run Analysis"
4. Download the PDF report if needed

---

## Troubleshooting

**CORS issues?** Backend needs to run on port 8000.

**CSV not working?** Make sure dates are in `YYYY-MM-DD` format and values are numbers.

**No forecast showing?** Prophet needs enough historical data to detect patterns. Try uploading more rows.

---

## What's Next

- Multi-variate forecasting (add weather, holidays, etc.)
- Database integration (PostgreSQL/BigQuery)
- User accounts and saved forecasts

---

<p align="center">Made for anyone who wants to see what's coming next in their data.</p>
