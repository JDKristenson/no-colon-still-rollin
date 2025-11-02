# 🚨 FIX REGISTRATION - Step by Step

## Problem
Registration fails with "internal error" because:
1. **Vercel frontend** doesn't have `VITE_API_URL` configured
2. **Backend** might have database issues

---

## ✅ STEP 1: Set Vercel Environment Variable (CRITICAL!)

**This is why registration fails - frontend can't reach backend!**

1. Go to: https://vercel.com/kristenson-7537s-projects/no-colon-still-rollin/settings/environment-variables

2. Click **"Add New"**

3. Fill in:
   - **Key**: `VITE_API_URL`
   - **Value**: `https://no-colon-still-rollin-production.up.railway.app`
   - **Environment**: Check **Production** ✅
   - **Preview**: Check **Preview** ✅ (optional but recommended)

4. Click **"Save"**

5. It will prompt to redeploy - click **"Redeploy"**

**This is the #1 issue - do this FIRST!**

---

## ✅ STEP 2: Update Railway CORS

After you know your Vercel URL:

1. Go to: https://railway.com/project/fd467ce0-7ede-45a1-aefd-9a35d8e47026/service/be163e70-674e-4cca-bd02-c71e0d04fb07/variables

2. Find `CORS_ORIGINS` variable

3. Edit it to include your Vercel URL:
   
   Format: `http://localhost:5173,http://localhost:3000,https://YOUR-VERCEL-URL`
   
   (Replace `YOUR-VERCEL-URL` with your actual Vercel domain)

4. Save (Railway auto-restarts)

---

## ✅ STEP 3: Check Backend Database

If registration still fails after Step 1, check Railway logs:

1. Go to: https://railway.com/project/fd467ce0-7ede-45a1-aefd-9a35d8e47026/service/be163e70-674e-4cca-bd02-c71e0d04fb07/logs

2. Look for error messages around registration

3. Common issues:
   - "relation 'users' does not exist" → Need to run migrations
   - Database connection errors → Check DATABASE_URL in Railway variables

---

## ✅ STEP 4: Test Again

After completing Steps 1-2:

1. Wait 1-2 minutes for deployments to finish
2. Open your Vercel app URL
3. Open browser DevTools (F12) → Console tab
4. Try to register
5. Check console for error messages - they'll now show the API URL

---

## Icon Not Showing?

The icon file is at: `/frontend/public/assets/rod-of-asclepius.svg`

If it's not showing:
1. Open browser DevTools (F12) → Network tab
2. Look for 404 errors on `/assets/rod-of-asclepius.svg`
3. Check that the file was deployed (it should be - we committed it)

---

## Quick Test Commands

**Test backend directly:**
```bash
curl -X POST https://no-colon-still-rollin-production.up.railway.app/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@test.com","password":"test123","name":"Test"}'
```

If this works, backend is fine - issue is frontend config.
If this fails, backend has issues - check Railway logs.

