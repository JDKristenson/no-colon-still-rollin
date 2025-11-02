# Run Database Migration on Railway

## Problem
The genetic marker tables don't exist, causing Railway backend to crash.

## Solution: Run Migration

### Option 1: Railway Terminal (Easiest)
1. Go to Railway Dashboard
2. Select your backend service
3. Click "Deployments" tab
4. Click on the latest deployment
5. Click "View Logs" or find "Terminal" button
6. In the terminal, run:
   ```bash
   cd backend
   alembic upgrade head
   ```
7. Wait for it to complete
8. Restart the service

### Option 2: Railway CLI (If you have it installed)
```bash
railway run --service backend alembic upgrade head
```

### Option 3: Add to Startup Script (Temporary)
If Railway has a startup hook, you could temporarily add:
```bash
cd backend && alembic upgrade head && python -m uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

## Expected Output
You should see:
```
INFO  [alembic.runtime.migration] Running upgrade add_email_verification -> add_genetic_markers, add genetic markers
```

## Verify Migration Worked
After running migration, check Railway logs for:
- ✅ No more "table doesn't exist" errors
- ✅ Service starts successfully
- ✅ Health endpoint responds

## Then Restart Service
- Railway → Service → Settings → Restart
- Wait 30 seconds
- Test your Vercel app again

