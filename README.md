# No Colon, Still Rollin' - Integrated Cancer Protocol & Workout System

**Version:** 3.0.0  
**Status:** Production Build

## Mission

Integrated cancer management platform combining evidence-based anti-cancer nutrition protocols with strategic workout programming designed to compete with cancer for glutamine—a key cancer fuel source.

## Tech Stack

- **Frontend:** React 18 + TypeScript + Vite + Tailwind CSS + shadcn/ui + Framer Motion
- **Backend:** FastAPI + PostgreSQL + SQLAlchemy + Alembic
- **Auth:** JWT-based authentication
- **Deployment:** Vercel (frontend) + Railway/Render (backend)

## Quick Start

### Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --reload
```

### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

## Project Structure

```
/
├── backend/          # FastAPI backend
├── frontend/        # React frontend
├── database/        # Migrations and seeds
└── docs/            # Documentation
```

## Features

- ✅ Premium UI/UX with Vitruvian Man visualization
- ✅ Nutrition protocol generation (9 anti-cancer foods)
- ✅ Intelligent workout programming with soreness tracking
- ✅ Complex glutamine competition scoring
- ✅ Meal recipes and exercise library
- ✅ Research integration
- ✅ Full export functionality

