# 🚀 INSTANT DEPLOYMENT - Copy & Paste Method

## Total Time: 3 Minutes

### STEP 1: Railway Backend (90 seconds)

1. **Click**: https://railway.app/new?template=blank&service=github
2. **Select repo**: `JDKristenson/no-colon-still-rollin`
3. **After deployment loads** → Click service → **Settings** tab:
   - Root Directory: `backend`
   - Build Command: `pip install -r requirements.txt`  
   - Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
4. **Variables** tab → Click **"+ New Variable"** → Add these 3:

```
DATABASE_URL = postgresql://postgres.wpyntnmjncdizglqedyl:2022FreshStart@aws-1-us-east-2.pooler.supabase.com:6543/postgres
```

```
SECRET_KEY = 0986f53c88aaca014f0fa1c140fd24e7ec5deef9d595652d65c71e7308a7a3e8
```

```
CORS_ORIGINS = https://your-app.vercel.app,http://localhost:5173
```

5. **Copy Railway URL** from the dashboard (top of service page)
   - Format: `https://xxx.railway.app`
   - **Save this URL!**

---

### STEP 2: Vercel Frontend (60 seconds)

1. **Click**: https://vercel.com/new
2. **Import** → Select: `JDKristenson/no-colon-still-rollin`
3. **Configure**:
   - Root Directory: `frontend`
   - Framework Preset: **Vite** (auto-detected)
   - Build Command: `npm run build` (auto)
   - Output Directory: `dist` (auto)
4. **Environment Variables** → Click **"+ Add"**:
   - Key: `VITE_API_URL`
   - Value: **[Paste your Railway URL from Step 1]**
5. **Deploy** → Wait ~30 seconds
6. **Copy Vercel URL** from dashboard
   - Format: `https://xxx.vercel.app`
   - **Save this URL!**

---

### STEP 3: Connect Everything (30 seconds)

1. **Go back to Railway** → Your service → **Variables**
2. **Edit `CORS_ORIGINS`** variable:
   - Replace `https://your-app.vercel.app` with your **actual Vercel URL**
   - Save (Railway auto-redeploys)

---

### STEP 4: Test (30 seconds)

1. **Visit your Vercel URL**
2. **Register** a new user
3. **Generate** a protocol
4. **Generate** a workout
5. **✅ DONE!**

---

## Quick Links

- **Railway**: https://railway.app/new
- **Vercel**: https://vercel.com/new
- **GitHub Repo**: https://github.com/JDKristenson/no-colon-still-rollin

---

**That's it! 3 minutes and you're live! 🎉**

