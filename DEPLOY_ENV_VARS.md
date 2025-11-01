# Deployment Environment Variables

## Backend (Railway) Environment Variables

Copy these into Railway Dashboard → Your Service → Variables:

```
DATABASE_URL=postgresql://postgres.wpyntnmjncdizglqedyl:2022FreshStart@aws-1-us-east-2.pooler.supabase.com:6543/postgres
SECRET_KEY=c4f8e9b2a1d3f5a7c9e1b3d5f7a9c1e3b5d7f9a1c3e5b7d9f1a3c5e7b9d1f3a
CORS_ORIGINS=https://your-app.vercel.app,http://localhost:5173
```

**Note**: Replace `https://your-app.vercel.app` with your actual Vercel URL after frontend deployment.

## Frontend (Vercel) Environment Variables

Copy this into Vercel Dashboard → Your Project → Settings → Environment Variables:

```
VITE_API_URL=https://your-backend.railway.app
```

**Note**: Replace `https://your-backend.railway.app` with your actual Railway backend URL.

## Quick Copy-Paste Commands

### For Railway (after deployment):
1. Go to Railway Dashboard → Your Service → Variables
2. Add each variable
3. Update CORS_ORIGINS with Vercel URL

### For Vercel (after deployment):
1. Go to Vercel Dashboard → Your Project → Settings → Environment Variables
2. Add VITE_API_URL
3. Redeploy frontend

---

**All set! Deploy backend first, then frontend, then update the URLs.**

