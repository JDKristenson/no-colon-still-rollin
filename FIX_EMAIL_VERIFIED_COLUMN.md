# 🔴 CRITICAL: Fix Missing email_verified Column

## The Problem
Backend is crashing with:
```
column users.email_verified does not exist
```

This happens because:
1. The User model expects `email_verified` column
2. The migration `add_email_verification_fields` hasn't run on Railway
3. When SQLAlchemy queries users, it tries to SELECT all columns including `email_verified`

## The Fix (Already Deployed)

I've made two fixes:

### 1. Idempotent Migration
The migration now checks if columns exist before adding them, so it's safe to run multiple times.

### 2. Fallback Query Handling
Auth endpoints now gracefully handle missing columns with fallback SQL queries.

## What You Need To Do

### Option 1: Wait for Auto-Migration (Recommended)
The `start.sh` script should run `alembic upgrade head` automatically. Wait 2-3 minutes for Railway to deploy.

### Option 2: Run Migration Manually (If auto-migration didn't work)
1. Railway Dashboard → Your Service → Deployments → Latest
2. Click "Shell" or "Terminal"
3. Run:
   ```bash
   cd backend
   alembic upgrade head
   ```
4. Verify it completes successfully
5. Restart Railway service

## Verify Fix

After migration runs, test:
```bash
curl https://no-colon-still-rollin-production.up.railway.app/api/health
```

Should return: `{"status":"healthy"}`

Then try registration/login in your Vercel app.

## Migration Status

Check which migrations have run:
```bash
cd backend
alembic current
alembic history
```

Should show:
- `4927cedb7907` (initial tables)
- `add_email_verification` (email fields)
- `add_genetic_markers` (genetic marker tables)

If `add_email_verification` is missing, that's the problem!

