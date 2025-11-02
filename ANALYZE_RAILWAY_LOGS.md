# How to Analyze Railway Logs

## Common Errors to Look For

### 1. Database Migration Errors
```
sqlalchemy.exc.ProgrammingError: (psycopg2.errors.UndefinedTable) relation "genetic_markers" does not exist
```
**Fix:** Run `alembic upgrade head` in Railway terminal

### 2. Import Errors
```
ModuleNotFoundError: No module named 'app.models.genetic_marker'
```
**Fix:** Check if file exists, verify imports

### 3. Missing Dependencies
```
ModuleNotFoundError: No module named 'openpyxl'
```
**Fix:** `pip install openpyxl` or check requirements.txt

### 4. Database Connection Errors
```
sqlalchemy.exc.OperationalError: could not connect to server
```
**Fix:** Check DATABASE_URL in Railway environment variables

### 5. Startup Crashes
```
AttributeError: 'NoneType' object has no attribute...
```
**Fix:** Usually a missing table or null reference

### 6. CORS Not Applied
No specific error, but requests fail with Network Error
**Fix:** Restart Railway service after setting CORS_ORIGINS

## Quick Diagnostic Commands

Once you share the logs, I can:
1. Identify the specific error
2. Provide exact fix steps
3. Check if migration is needed
4. Verify all dependencies are installed

## What to Share
- The last 50-100 lines of Railway logs
- Any error messages (especially red/highlighted ones)
- Startup errors
- Any "Traceback" or "Exception" messages

