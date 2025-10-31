# Deployment Guide

## Quick Deploy to Vercel

### Prerequisites
- Vercel account
- PostgreSQL database (Vercel Postgres, Supabase, or Railway)
- GitHub repository connected to Vercel

### Steps

1. **Set up PostgreSQL Database**
   - Create a PostgreSQL database (Vercel Postgres recommended)
   - Get connection string

2. **Configure Environment Variables in Vercel**
   ```
   DATABASE_URL=postgresql://user:pass@host:port/db
   SECRET_KEY=your-secret-key-here
   CORS_ORIGINS=https://yourdomain.com
   ```

3. **Deploy Frontend**
   - Connect GitHub repo to Vercel
   - Set root directory to `frontend`
   - Build command: `npm run build`
   - Output directory: `dist`

4. **Deploy Backend**
   - Option A: Use Vercel serverless functions
   - Option B: Deploy separately to Railway/Render

## Alternative: Railway Deployment

1. **Create Railway Project**
   - Connect GitHub repo
   - Add PostgreSQL service

2. **Deploy Backend**
   - Set root directory to `backend`
   - Install command: `pip install -r requirements.txt`
   - Start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

3. **Run Migrations**
   ```bash
   alembic upgrade head
   ```

4. **Seed Data**
   ```bash
   python scripts/seed_database.py
   ```

## Environment Variables

Create `.env` file in backend:
```
DATABASE_URL=postgresql://...
SECRET_KEY=your-secret-key
CORS_ORIGINS=http://localhost:5173,https://yourdomain.com
```

## Database Setup

1. **Run Migrations**
   ```bash
   cd backend
   alembic upgrade head
   ```

2. **Seed Database**
   ```bash
   python scripts/seed_database.py
   ```

## Production Checklist

- [ ] Environment variables configured
- [ ] Database migrations run
- [ ] Seed data loaded
- [ ] CORS origins updated
- [ ] SECRET_KEY changed from default
- [ ] Frontend API base URL updated
- [ ] SSL/HTTPS enabled
- [ ] Error tracking configured (optional)

