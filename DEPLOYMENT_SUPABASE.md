# Deployment Guide - Supabase

## Overview

This guide walks you through deploying **No Colon, Still Rollin'** using:
- **Supabase** - PostgreSQL database
- **Vercel** - Frontend deployment
- **Railway** or **Render** - Backend API (recommended) OR Vercel serverless functions

## Step 1: Set Up Supabase Database

### 1.1 Create Supabase Project

1. Go to [Supabase Dashboard](https://app.supabase.com)
2. Click "New Project"
3. Name: `no-colon-still-rollin`
4. Set database password (save this!)
5. Choose region closest to you
6. Wait for project to initialize (~2 minutes)

### 1.2 Get Connection String

1. Go to **Settings** → **Database**
2. Scroll to "Connection string"
3. Copy the **URI** connection string
4. Format: `postgresql://postgres:[YOUR-PASSWORD]@db.[PROJECT-REF].supabase.co:5432/postgres`

### 1.3 Update Environment Variables in Supabase

1. Go to **Settings** → **API**
2. Note your `project_url` and `anon` key (for future use if needed)

## Step 2: Configure Backend for Supabase

### 2.1 Update Backend Config

Create `.env` file in `backend/`:

```bash
DATABASE_URL=postgresql://postgres:[YOUR-PASSWORD]@db.[PROJECT-REF].supabase.co:5432/postgres
SECRET_KEY=your-super-secret-key-change-this-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=10080
CORS_ORIGINS=https://your-vercel-app.vercel.app,http://localhost:5173
PROJECT_NAME=No Colon, Still Rollin'
```

### 2.2 Run Migrations Locally (Test Connection)

```bash
cd backend
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt

# Update alembic.ini with your DATABASE_URL or use env variable
alembic upgrade head
```

### 2.3 Seed Database

```bash
python scripts/seed_database.py
```

Verify in Supabase Dashboard → **Table Editor** that tables are created and seeded.

## Step 3: Deploy Backend (Option A: Railway - Recommended)

### 3.1 Create Railway Project

1. Go to [Railway.app](https://railway.app)
2. "New Project" → "Deploy from GitHub repo"
3. Select your repository
4. Add service → "Empty Service"

### 3.2 Configure Railway

**Settings:**
- Root Directory: `backend`
- Build Command: `pip install -r requirements.txt`
- Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

**Environment Variables:**
```
DATABASE_URL=[Your Supabase connection string]
SECRET_KEY=[Generate a secure random string]
CORS_ORIGINS=https://your-vercel-app.vercel.app
```

### 3.3 Run Migrations on Railway

After deployment, run migrations:
1. Railway dashboard → Service → "View Logs"
2. Click "Shell" or use Railway CLI:
```bash
railway run alembic upgrade head
```

Or add to your deployment script (create `railway.json`):

```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "uvicorn app.main:app --host 0.0.0.0 --port $PORT",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

## Step 4: Deploy Backend (Option B: Render)

### 4.1 Create Render Web Service

1. Go to [Render Dashboard](https://dashboard.render.com)
2. "New" → "Web Service"
3. Connect your GitHub repository

### 4.2 Configure Render

**Settings:**
- Name: `nocolon-backend`
- Root Directory: `backend`
- Environment: `Python 3`
- Build Command: `pip install -r requirements.txt`
- Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

**Environment Variables:**
```
DATABASE_URL=[Your Supabase connection string]
SECRET_KEY=[Generate a secure random string]
CORS_ORIGINS=https://your-vercel-app.vercel.app
PYTHON_VERSION=3.11
```

### 4.3 Run Migrations on Render

After first deployment:
1. Render dashboard → Service → "Shell"
2. Run: `alembic upgrade head`
3. Run: `python scripts/seed_database.py`

## Step 5: Deploy Frontend to Vercel

### 5.1 Connect Repository

1. Go to [Vercel Dashboard](https://vercel.com)
2. "Add New" → "Project"
3. Import your GitHub repository

### 5.2 Configure Vercel

**Project Settings:**
- Framework Preset: Vite
- Root Directory: `frontend`
- Build Command: `npm run build`
- Output Directory: `dist`

**Environment Variables:**
```
VITE_API_URL=https://your-railway-or-render-backend-url.railway.app
```

### 5.3 Update Frontend API Base URL

Update `frontend/src/lib/api.ts` for production:

```typescript
const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || '/api',
  // ... rest of config
})
```

Or set in Vercel environment variables and use `import.meta.env.VITE_API_URL`.

## Step 6: Update CORS Settings

### Backend CORS Update

Update `backend/app/core/config.py` to include your Vercel URL:

```python
CORS_ORIGINS: List[str] = [
    "http://localhost:5173",
    "https://your-app.vercel.app",  # Add your Vercel URL
]
```

Or set via environment variable in Railway/Render.

## Step 7: Final Verification

### 7.1 Database Check

1. Supabase Dashboard → Table Editor
2. Verify tables exist: `users`, `foods`, `exercises`, `muscle_groups`, etc.
3. Check seed data is loaded

### 7.2 Backend Check

1. Visit `https://your-backend.railway.app/docs`
2. Should see FastAPI Swagger UI
3. Test `/health` endpoint

### 7.3 Frontend Check

1. Visit your Vercel URL
2. Register/login
3. Test generating protocol
4. Test generating workout

## Step 8: Production Optimizations

### 8.1 Enable Row Level Security (Optional)

In Supabase SQL Editor:

```sql
-- Example: Enable RLS on users table
ALTER TABLE users ENABLE ROW LEVEL SECURITY;

-- Create policy (users can only see their own data)
CREATE POLICY "Users can view own data" ON users
  FOR SELECT USING (auth.uid() = id);
```

### 8.2 Set Up Database Backups

Supabase automatically backs up, but verify:
1. Settings → Database
2. Check backup schedule
3. Set up manual backup if needed

### 8.3 Monitoring

**Supabase:**
- Monitor database usage in Dashboard
- Set up alerts for storage/queries

**Railway/Render:**
- Monitor logs
- Set up uptime monitoring (UptimeRobot, etc.)

**Vercel:**
- Check analytics
- Monitor build logs

## Troubleshooting

### Database Connection Issues

**Error: "connection refused"**
- Check Supabase project is active
- Verify connection string (especially password)
- Check IP allowlist in Supabase (should allow all for now)

**Error: "relation does not exist"**
- Run migrations: `alembic upgrade head`
- Verify migrations ran successfully

### Backend Issues

**Error: "Module not found"**
- Ensure `requirements.txt` is complete
- Check build logs in Railway/Render

**Error: "Port already in use"**
- Railway/Render handles this automatically
- Don't hardcode ports, use `$PORT`

### Frontend Issues

**API calls failing**
- Check CORS origins include your Vercel URL
- Verify `VITE_API_URL` is set correctly
- Check browser console for errors

**Build fails**
- Check Node version (should be 18+)
- Verify all dependencies in `package.json`
- Check build logs in Vercel

## Quick Deploy Checklist

- [ ] Supabase project created
- [ ] Database connection string copied
- [ ] Backend deployed (Railway/Render)
- [ ] Migrations run on production database
- [ ] Database seeded
- [ ] Frontend deployed (Vercel)
- [ ] Environment variables set in all services
- [ ] CORS configured correctly
- [ ] Test registration/login
- [ ] Test protocol generation
- [ ] Test workout generation
- [ ] Verify all features working

## Cost Estimate

**Free Tier (for development/testing):**
- Supabase: Free (500MB database, 2GB bandwidth)
- Railway: $5/month (or free tier if available)
- Render: Free tier available
- Vercel: Free (hobby plan)

**Total: ~$5/month or free** (depending on usage)

## Support

- Supabase Docs: https://supabase.com/docs
- Railway Docs: https://docs.railway.app
- Render Docs: https://render.com/docs
- Vercel Docs: https://vercel.com/docs

---

**Ready to deploy! Follow these steps in order and you'll have a production system running.**

