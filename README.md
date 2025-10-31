# No Colon, Still Rollin' - Integrated Cancer Protocol & Workout System

**Version:** 3.0.0  
**Status:** Production Ready

## Mission

Integrated cancer management platform combining evidence-based anti-cancer nutrition protocols with strategic workout programming designed to compete with cancer for glutamine—a key cancer fuel source.

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Node.js 18+
- PostgreSQL 14+
- npm or yarn

### Backend Setup

```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Create .env file
cp ../.env.example .env
# Edit .env with your DATABASE_URL and SECRET_KEY

# Run migrations
alembic upgrade head

# Seed database
python scripts/seed_database.py

# Start server
uvicorn app.main:app --reload
```

Backend runs at: http://localhost:8000

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

Frontend runs at: http://localhost:5173

## 📁 Project Structure

```
/
├── backend/              # FastAPI backend
│   ├── app/
│   │   ├── main.py      # FastAPI app
│   │   ├── models/      # SQLAlchemy models
│   │   ├── api/         # API routes
│   │   ├── algorithms/  # Business logic
│   │   └── core/        # Config, database, security
│   ├── alembic/         # Database migrations
│   └── scripts/         # Utility scripts
├── frontend/            # React frontend
│   ├── src/
│   │   ├── components/  # React components
│   │   ├── pages/       # Page components
│   │   └── lib/         # Utilities
│   └── public/
├── database/
│   └── seeds/          # Seed data JSON files
└── docs/               # Documentation
```

## 🎯 Features

### ✅ Complete Feature Set

- **Premium UI/UX** - Slick, professional interface with Vitruvian Man visualization
- **Authentication** - Multi-user JWT-based auth system
- **Dashboard** - Unified command center with real-time metrics
- **Nutrition Protocol** - 9 anti-cancer foods with daily generation
- **Workout System** - Intelligent rotation maintaining continuous soreness
- **Soreness Tracker** - Interactive Vitruvian Man with muscle group tracking
- **Exercise Library** - 22+ exercises with form cues
- **Progress Analytics** - Weight trends, adherence charts, health metrics
- **Research Library** - Evidence-based research database
- **Export Functionality** - JSON, CSV, and complete report exports
- **Coaching System** - Dynamic, personalized messages

### Complex Algorithms

- **Glutamine Competition Score** - Multi-factor calculation
- **Workout Rotation Optimizer** - Maintains continuous soreness coverage
- **Protein Target Adjuster** - Dynamic adjustment based on soreness state
- **Soreness Predictor** - Intensity-based duration prediction

## 🔐 Default Credentials

**Test User:**
- Email: `jesse@example.com`
- Password: `password123`

*Change immediately in production!*

## 🌐 Deployment

**Recommended: Supabase + Vercel + Railway**

See [DEPLOYMENT_SUPABASE.md](./DEPLOYMENT_SUPABASE.md) for detailed Supabase deployment instructions.

### Quick Setup

1. **Supabase**: Create project, get connection string
2. **Railway/Render**: Deploy backend, set DATABASE_URL to Supabase
3. **Vercel**: Deploy frontend, set VITE_API_URL to backend URL
4. Run migrations: `alembic upgrade head`
5. Seed database: `python scripts/seed_database.py`

For alternative deployment methods, see [DEPLOYMENT.md](./DEPLOYMENT.md).

## 📊 Database

- **Development:** PostgreSQL (local or cloud)
- **Migrations:** Alembic
- **Seed Data:** 9 foods, 22 exercises, 6 muscle groups

## 🛠️ Tech Stack

**Frontend:**
- React 18 + TypeScript
- Vite
- Tailwind CSS
- shadcn/ui
- Framer Motion
- Recharts
- React Query

**Backend:**
- FastAPI
- PostgreSQL
- SQLAlchemy
- Alembic
- Pydantic
- JWT Authentication

## 📝 API Documentation

API runs at `/api` with OpenAPI docs at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 🎨 Design Philosophy

- **Premium UI** - Not home-baked. Professional, slick, impressive.
- **Smooth Animations** - Framer Motion throughout
- **Responsive** - Mobile-first design
- **Accessible** - WCAG guidelines
- **Fast** - Optimized performance

## 🔬 Scientific Basis

The system is based on the glutamine competition theory:
- Cancer cells fuel on glucose and glutamine
- Sore muscles consume glutamine
- Continuous muscle soreness creates metabolic competition
- Combined with ketogenic nutrition (glucose restriction)
- Dual-front metabolic strategy against cancer

## ⚠️ Medical Disclaimer

This system is for tracking and hypothesis testing. It is not medical advice. Always consult with oncologists and healthcare providers.

## 📄 License

Private use only.

## 👥 Authors

Built for Jesse Mills by JD Kristenson
October 2025

---

**Let's save a life. 💪**
