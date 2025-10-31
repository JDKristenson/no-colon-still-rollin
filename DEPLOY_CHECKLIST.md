# Supabase Deployment Checklist

## Pre-Deployment

- [ ] Supabase account ready
- [ ] GitHub repository pushed (all code committed)
- [ ] Railway/Render account created (for backend)
- [ ] Vercel account ready (for frontend)

## Step 1: Supabase Setup (5 minutes)

- [ ] Create new Supabase project
- [ ] Copy database connection string (URI format)
- [ ] Note project URL and anon key (for reference)
- [ ] Test connection string locally (optional but recommended)

**Connection String Format:**
```
postgresql://postgres.[ref]:[password]@aws-0-[region].pooler.supabase.com:6543/postgres
```
*Use Transaction Pooler (port 6543) for better serverless compatibility*

## Step 2: Local Database Setup (10 minutes)

- [ ] Create `backend/.env` file with Supabase connection string
- [ ] Install backend dependencies: `pip install -r requirements.txt`
- [ ] Run migrations: `alembic upgrade head`
- [ ] Seed database: `python scripts/seed_database.py`
- [ ] Verify tables in Supabase Dashboard → Table Editor
- [ ] Test local backend: `uvicorn app.main:app --reload`
- [ ] Test API at `http://localhost:8000/docs`

## Step 3: Deploy Backend to Railway (15 minutes)

- [ ] Create Railway account/project
- [ ] Connect GitHub repository
- [ ] Create new service from repository
- [ ] Set root directory: `backend`
- [ ] Set environment variables:
  - `DATABASE_URL` = [Your Supabase connection string]
  - `SECRET_KEY` = [Generate: `openssl rand -hex 32`]
  - `CORS_ORIGINS` = [Will add after Vercel deploy]
- [ ] Deploy service
- [ ] Get Railway backend URL
- [ ] Test backend: Visit `https://your-backend.railway.app/docs`
- [ ] Run migrations on Railway (via shell or CLI)
- [ ] Seed database on Railway

**Alternative: Render**
- [ ] Create Render account
- [ ] New Web Service from GitHub
- [ ] Configure same as Railway
- [ ] Deploy and test

## Step 4: Deploy Frontend to Vercel (10 minutes)

- [ ] Create Vercel project from GitHub
- [ ] Set root directory: `frontend`
- [ ] Framework: Vite (auto-detected)
- [ ] Build command: `npm run build`
- [ ] Output directory: `dist`
- [ ] Set environment variable:
  - `VITE_API_URL` = `https://your-backend.railway.app`
- [ ] Deploy
- [ ] Get Vercel URL

## Step 5: Connect Services (5 minutes)

- [ ] Update backend CORS_ORIGINS with Vercel URL
- [ ] Redeploy backend (or update env var)
- [ ] Test frontend can reach backend
- [ ] Check browser console for CORS errors

## Step 6: Final Verification (10 minutes)

- [ ] Visit Vercel frontend URL
- [ ] Register new user
- [ ] Login successfully
- [ ] Generate nutrition protocol
- [ ] Generate workout plan
- [ ] Log soreness
- [ ] Check compliance tracking
- [ ] View dashboard metrics
- [ ] Test all navigation links
- [ ] Verify mobile responsiveness

## Step 7: Production Hardening

- [ ] Change default user password (if keeping test user)
- [ ] Verify SECRET_KEY is strong and unique
- [ ] Set up database backups schedule (Supabase handles this)
- [ ] Enable error logging/monitoring (optional)
- [ ] Set up uptime monitoring (UptimeRobot, etc.)
- [ ] Test error scenarios (network failures, etc.)
- [ ] Document production URLs and credentials securely

## Post-Deployment

- [ ] Share URLs with Jesse
- [ ] Set up regular database backups verification
- [ ] Monitor usage (Supabase dashboard)
- [ ] Plan for scaling if needed

## Troubleshooting Quick Reference

**Database Connection Issues:**
```bash
# Test connection locally
python -c "from app.core.database import engine; engine.connect(); print('✅ Connected')"
```

**Migration Issues:**
```bash
# On Railway/Render shell
alembic upgrade head
alembic current  # Check current revision
```

**CORS Issues:**
- Verify CORS_ORIGINS includes exact Vercel URL (with https://)
- Check browser console for specific CORS error
- Verify backend is sending correct CORS headers

**Build Issues:**
- Check Vercel build logs
- Verify Node version (18+)
- Check package.json dependencies

## Quick Commands Reference

```bash
# Local database setup
cd backend
source venv/bin/activate
alembic upgrade head
python scripts/seed_database.py

# Test backend locally
uvicorn app.main:app --reload

# Test frontend locally
cd frontend
npm run dev

# Generate secret key
openssl rand -hex 32

# Railway CLI (if using)
railway login
railway link
railway up
railway shell  # Run migrations here
```

---

**Estimated Total Time: ~45-60 minutes**

**Status: Ready to deploy when you are!** 🚀

