# Automated Deployment Guide

## Quick Deploy (All Automated)

Run the deployment script:
```bash
./deploy.sh
```

Or follow the manual steps below if you prefer.

## Backend Deployment (Railway)

### Option 1: Via Railway Dashboard (Easiest)

1. **Go to**: https://railway.app
2. **Login** with GitHub
3. **New Project** → **Deploy from GitHub repo**
4. **Select repository**: `no-colon-still-rollin`
5. **Add Service** → **GitHub Repo** → Select repo
6. **Settings**:
   - Root Directory: `backend`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
7. **Variables** tab → Add:
   ```
   DATABASE_URL=postgresql://postgres.wpyntnmjncdizglqedyl:2022FreshStart@aws-1-us-east-2.pooler.supabase.com:6543/postgres
   SECRET_KEY=[Will generate]
   CORS_ORIGINS=https://your-vercel-app.vercel.app
   ```
8. **Generate SECRET_KEY**: Railway can generate this, or run `openssl rand -hex 32`
9. **Deploy** → Get Railway URL

### Option 2: Via Railway CLI

```bash
# Install Railway CLI (if not installed)
curl -fsSL https://railway.app/install.sh | sh

# Login
railway login

# Initialize project
cd backend
railway init

# Link to existing project or create new
railway link

# Set environment variables
railway variables set DATABASE_URL="postgresql://postgres.wpyntnmjncdizglqedyl:2022FreshStart@aws-1-us-east-2.pooler.supabase.com:6543/postgres"
railway variables set SECRET_KEY="$(openssl rand -hex 32)"
railway variables set CORS_ORIGINS="https://your-vercel-app.vercel.app"

# Deploy
railway up
```

## Frontend Deployment (Vercel)

### Option 1: Via Vercel Dashboard

1. **Go to**: https://vercel.com
2. **Login** with GitHub
3. **Add New** → **Project**
4. **Import** from GitHub → Select `no-colon-still-rollin`
5. **Configure**:
   - Framework Preset: Vite
   - Root Directory: `frontend`
   - Build Command: `npm run build`
   - Output Directory: `dist`
6. **Environment Variables**:
   ```
   VITE_API_URL=https://your-railway-backend.railway.app
   ```
7. **Deploy** → Get Vercel URL

### Option 2: Via Vercel CLI

```bash
# Install Vercel CLI (if not installed)
npm install -g vercel

# Login
vercel login

# Deploy
cd frontend
vercel --prod

# Set environment variable
vercel env add VITE_API_URL production
# Enter: https://your-railway-backend.railway.app
```

## Post-Deployment

After both are deployed:

1. **Update Railway CORS_ORIGINS** with your actual Vercel URL
2. **Test**: Visit Vercel URL → Register/Login
3. **Verify**: Generate protocol, generate workout

## All Environment Variables

### Railway (Backend)
- `DATABASE_URL` = (Supabase connection string)
- `SECRET_KEY` = (Generated secure key)
- `CORS_ORIGINS` = (Your Vercel URL)

### Vercel (Frontend)
- `VITE_API_URL` = (Your Railway backend URL)

---

**Ready to deploy! Follow Option 1 for each (dashboard method is easiest).**

