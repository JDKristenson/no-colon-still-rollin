# One-Command Deployment (Almost!)

## Prerequisites
- Railway account: https://railway.app
- Vercel account: https://vercel.com
- Both connected to GitHub

## Fastest Path to Production

### Step 1: Deploy Backend (Railway) - 2 Minutes

**Option A: Railway Dashboard (Easiest)**
1. Go to: https://railway.app/new
2. Click **"Deploy from GitHub repo"**
3. Select: `JDKristenson/no-colon-still-rollin`
4. **After it deploys** → Click service → **Settings**:
   - Root Directory: `backend`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
5. **Variables** tab → Add these:
   ```
   DATABASE_URL=postgresql://postgres.wpyntnmjncdizglqedyl:2022FreshStart@aws-1-us-east-2.pooler.supabase.com:6543/postgres
   SECRET_KEY=0986f53c88aaca014f0fa1c140fd24e7ec5deef9d595652d65c71e7308a7a3e8
   CORS_ORIGINS=https://your-app.vercel.app
   ```
6. **Get Railway URL** (shown in dashboard, e.g., `https://xxx.railway.app`)

**Option B: Railway CLI**
```bash
cd backend
railway login
railway init
railway link  # or create new project
railway variables set DATABASE_URL="postgresql://postgres.wpyntnmjncdizglqedyl:2022FreshStart@aws-1-us-east-2.pooler.supabase.com:6543/postgres"
railway variables set SECRET_KEY="0986f53c88aaca014f0fa1c140fd24e7ec5deef9d595652d65c71e7308a7a3e8"
railway up
```

### Step 2: Deploy Frontend (Vercel) - 1 Minute

**Option A: Vercel Dashboard (Easiest)**
1. Go to: https://vercel.com/new
2. **Import** → Select `JDKristenson/no-colon-still-rollin`
3. **Configure**:
   - Root Directory: `frontend`
   - Framework: Vite (auto-detected)
4. **Environment Variables**:
   ```
   VITE_API_URL=https://your-railway-url.railway.app
   ```
   (Use your Railway URL from Step 1)
5. **Deploy** → Get Vercel URL

**Option B: Vercel CLI**
```bash
cd frontend
vercel login
vercel --prod
# When prompted for environment variables:
# VITE_API_URL = https://your-railway-url.railway.app
```

### Step 3: Connect Everything - 30 Seconds

1. **Go back to Railway** → Variables
2. **Update CORS_ORIGINS** with your Vercel URL:
   ```
   CORS_ORIGINS=https://your-actual-vercel-url.vercel.app,http://localhost:5173
   ```
3. **Railway will auto-redeploy**

### Step 4: Test - 1 Minute

1. Visit your Vercel URL
2. Register new user
3. Generate protocol
4. Generate workout
5. ✅ Done!

---

## Total Time: ~5 Minutes

**That's it! Your system is live and ready to save a life! 🚀**

