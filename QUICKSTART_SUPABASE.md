# 🚀 Quick Start: Deploy to Supabase in 30 Minutes

## Prerequisites
- Supabase account ✅ (you have this)
- GitHub repo pushed ✅ (done)
- 30 minutes

## Step-by-Step

### 1. Supabase Database (5 min)

1. Go to [supabase.com/dashboard](https://supabase.com/dashboard)
2. **New Project** → Name it `no-colon-still-rollin`
3. Set password (save it!)
4. Wait ~2 min for setup
5. **Settings → Database → Connection string → URI**
6. Copy the connection string (Transaction Pooler version recommended)

### 2. Test Connection Locally (5 min)

```bash
cd backend
cp ../.env.example .env
# Edit .env and paste your Supabase connection string:
# DATABASE_URL=postgresql://postgres.[ref]:[password]@aws-0-[region].pooler.supabase.com:6543/postgres

python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Run migrations
alembic upgrade head

# Seed database
python scripts/seed_database.py
```

✅ Verify: Go to Supabase Dashboard → Table Editor → See tables created

### 3. Deploy Backend to Railway (10 min)

1. Go to [railway.app](https://railway.app)
2. **New Project → Deploy from GitHub**
3. Select your repo
4. **Add Service → GitHub Repo → Select repo**
5. **Settings:**
   - Root Directory: `backend`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
6. **Variables tab:**
   ```
   DATABASE_URL = [Your Supabase connection string]
   SECRET_KEY = [Run: openssl rand -hex 32]
   CORS_ORIGINS = https://your-app.vercel.app  (add after step 4)
   ```
7. Deploy → Get your Railway URL (e.g., `https://xxx.railway.app`)
8. **Shell tab → Run:**
   ```bash
   alembic upgrade head
   python scripts/seed_database.py
   ```

✅ Test: Visit `https://xxx.railway.app/docs` → See FastAPI docs

### 4. Deploy Frontend to Vercel (10 min)

1. Go to [vercel.com](https://vercel.com)
2. **Add New → Project → Import from GitHub**
3. Select your repo
4. **Configure:**
   - Framework: Vite (auto)
   - Root Directory: `frontend`
   - Build Command: `npm run build`
   - Output Directory: `dist`
5. **Environment Variables:**
   ```
   VITE_API_URL = https://xxx.railway.app
   ```
6. Deploy → Get Vercel URL

### 5. Connect Everything (5 min)

1. **Railway → Your Service → Variables:**
   - Update `CORS_ORIGINS` with your Vercel URL
   - Redeploy (or just save - auto redeploys)

2. **Test:**
   - Visit Vercel URL
   - Register/Login
   - Generate protocol
   - Generate workout

## ✅ Done!

Your system is live:
- Frontend: `https://your-app.vercel.app`
- Backend: `https://xxx.railway.app`
- Database: Supabase (managed)

## Need Help?

- **Database issues?** Check Supabase Dashboard → Logs
- **Backend issues?** Check Railway → Deployments → Logs
- **Frontend issues?** Check Vercel → Deployments → Logs
- **CORS errors?** Verify CORS_ORIGINS includes exact Vercel URL

## Next Steps

- Share URLs with Jesse
- Test all features
- Monitor Supabase usage
- Set up backups (Supabase handles this automatically)

---

**You're ready to save a life. Let's go! 💪**

