# BI Dashboard — Business Intelligence Analytics Portal

A modern enterprise Business Intelligence Dashboard for POS data analytics, built with **FastAPI** (Python) and **React + TypeScript**.

## 🚀 Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | FastAPI, SQLAlchemy 2.x, Python 3.11+ |
| Frontend | React 18, TypeScript, Vite |
| Database | SQL Server (ODBC Driver 17+) |
| Styling | Tailwind CSS v3, Glassmorphism |
| Charts | Recharts |
| Auth | JWT (python-jose + bcrypt) |
| Data Fetching | @tanstack/react-query, Axios |

## 📁 Project Structure

```
├── backend/          # FastAPI backend
│   ├── app/
│   │   ├── auth/     # JWT authentication & RBAC
│   │   ├── models/   # SQLAlchemy models
│   │   ├── routers/  # API endpoints
│   │   ├── schemas/  # Pydantic schemas
│   │   ├── services/ # Business logic
│   │   └── utils/    # Shared utilities
│   └── requirements.txt
├── frontend/         # React + TypeScript frontend
│   ├── src/
│   │   ├── api/      # API client & hooks
│   │   ├── components/  # Reusable UI components
│   │   ├── context/  # Auth, Theme, Filter contexts
│   │   ├── pages/    # Dashboard pages
│   │   └── types/    # TypeScript types
│   └── package.json
├── database/         # SQL scripts & schema docs
├── reports/          # PDF report templates
└── exports/          # Generated export files
```

## 🏁 Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+
- SQL Server with ODBC Driver 17+

### Backend Setup

```bash
cd backend
python -m venv venv
venv\Scripts\activate       # Windows
pip install -r requirements.txt

# Copy and configure environment
copy .env.example .env
# Edit .env with your SQL Server connection details

# Start the backend
uvicorn app.main:app --reload --port 8000
```

On first startup, the app will:
1. Create `dashboard_users` and `dashboard_audit_log` tables
2. Create a default admin user: `admin / admin123`

To seed sample data, call: `POST http://localhost:8000/api/v1/seed`

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

Open **http://localhost:5173** and login with `admin / admin123`.

## 🔑 Default Credentials

| Username | Password | Role |
|----------|----------|------|
| admin | admin123 | Super Admin |

## 👥 Role-Based Access

| Role | Access |
|------|--------|
| Super Admin | Full access, user management |
| Branch Manager | Own branch data only |
| Accountant | Financial data, all branches |
| Auditor | Read-only, all data + audit trail |

## 📊 API Documentation

Once the backend is running, visit:
- Swagger UI: http://localhost:8000/api/docs
- ReDoc: http://localhost:8000/api/redoc

## 📦 Key API Endpoints

| Endpoint | Description |
|----------|-------------|
| `POST /api/v1/auth/login` | Login, returns JWT |
| `GET /api/v1/dashboard/summary` | Executive KPIs |
| `GET /api/v1/dashboard/payment-breakdown` | Payment method split |
| `GET /api/v1/dashboard/trends` | Daily sales trends |
| `GET /api/v1/sales/trends?period=daily` | Sales analytics |
| `GET /api/v1/branches/compare` | Branch comparison |
| `GET /api/v1/exports/pdf` | Export PDF report |
| `GET /api/v1/exports/excel` | Export Excel report |
