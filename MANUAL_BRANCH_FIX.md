# Manual Railway Branch Fix

## The Problem
Railway is watching the **"master"** branch, but our repo uses **"main"** branch.

## Quick Fix (30 seconds)

1. Open: https://railway.com/project/fd467ce0-7ede-45a1-aefd-9a35d8e47026/service/be163e70-674e-4cca-bd02-c71e0d04fb07/settings?environmentId=314d8f19-54de-45a9-a3b2-24e9284bc26d#source

2. Scroll down to **"Branch connected to production"** section

3. Click the dropdown that shows **"master"**

4. Select **"main"** from the list

5. ✅ Railway will automatically trigger a new deployment from the correct branch!

## What's Ready
- ✅ Procfile with start command: `web: uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- ✅ Root Directory: `/backend` 
- ✅ backend/main.py entry point
- ✅ All code pushed to main branch

Once you change the branch, deployment should succeed! 🚀

