# Fix Network Error - Backend Connection Issue

## Problem
Frontend showing "Network Error" when trying to connect to Railway backend.

## Quick Fix Steps

### 1. Check Railway Service Status
- Go to Railway dashboard
- Check if your service is running
- Look for any crash logs or errors

### 2. Verify CORS Configuration in Railway
Set `CORS_ORIGINS` environment variable in Railway to:
```
*
```
Or your specific Vercel URL:
```
https://your-app.vercel.app
```

### 3. Restart Railway Service
- In Railway dashboard: Service → Settings → Restart
- Or trigger a new deployment

### 4. Check Railway Logs
Look for:
- Database connection errors
- Migration errors
- Import errors from new genetic marker models

### 5. Verify Backend is Accessible
Test these endpoints:
- `https://no-colon-still-rollin-production.up.railway.app/health`
- `https://no-colon-still-rollin-production.up.railway.app/api/health`

### 6. Run Database Migration (if needed)
If you see migration errors in Railway logs, connect to Railway terminal and run:
```bash
cd backend
alembic upgrade head
```

### 7. Check Frontend API URL
Verify your Vercel environment variable:
- Variable: `VITE_API_URL`
- Value: `https://no-colon-still-rollin-production.up.railway.app`

## Most Likely Issues

1. **Backend crashed** - Check Railway logs for Python errors
2. **CORS blocking** - Set `CORS_ORIGINS=*` in Railway
3. **Migration not run** - Genetic marker tables don't exist yet
4. **Service not running** - Railway service might have stopped

## Emergency CORS Fix
If you need to get it working immediately, add this to Railway environment variables:
```
CORS_ORIGINS=*
```
This allows all origins (safe for development, should restrict in production).

