# Debug Backend Network Error

## Issue
Network error persists even though CORS_ORIGINS=* is set in Railway.

## Possible Causes

### 1. Backend Service Crashed
The Railway service might have crashed due to:
- Missing database migration (genetic marker tables)
- Import error from new genetics endpoint
- Database connection failure

### 2. Check Railway Logs
Go to Railway → Your Service → Deployments → Latest → View Logs

Look for:
- `ModuleNotFoundError` - Missing imports
- `Table doesn't exist` - Migration not run
- `SyntaxError` or `ImportError` - Code issues

### 3. Run Database Migration
If you see migration errors:
```bash
# In Railway terminal or connect via CLI
cd backend
alembic upgrade head
```

### 4. Verify Backend is Running
Test these endpoints:
```bash
# Health check (no auth needed)
curl https://no-colon-still-rollin-production.up.railway.app/health

# Should return: {"status":"healthy"}

# API health (no auth needed)  
curl https://no-colon-still-rollin-production.up.railway.app/api/health

# API endpoint (should return 401 without auth)
curl https://no-colon-still-rollin-production.up.railway.app/api/dashboard
```

### 5. Check for Import Errors
New genetic marker code might have import issues. Check Railway logs for:
- `from app.models.genetic_marker import ...`
- `from app.core.signatera_parser import ...`
- `from app.algorithms.glutamine import get_active_markers`

### 6. Restart Railway Service
Even if nothing changed, sometimes a restart fixes connection issues:
- Railway → Service → Settings → Restart

### 7. Check Database Connection
Verify DATABASE_URL is set correctly in Railway variables.

## Quick Diagnostic Commands
Run these locally to check for import issues:
```bash
cd backend
python3 -c "from app.models.genetic_marker import GeneticMarker; print('OK')"
python3 -c "from app.core.signatera_parser import parse_signatera_excel; print('OK')"
python3 -c "from app.api.v1.endpoints import genetics; print('OK')"
```

If any fail, that's likely the issue causing Railway to crash.

