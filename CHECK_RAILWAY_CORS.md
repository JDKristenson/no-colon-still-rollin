# Check Railway CORS Configuration

## Steps to Verify CORS is Working

### 1. Check Railway Environment Variables
Go to Railway → Your Service → Variables
- Confirm `CORS_ORIGINS=*` is set
- If it exists, note the value

### 2. Check Service Status
- Railway → Service → Is it "Active"?
- Check deployment status - is it deployed?

### 3. Restart Service (Important!)
Even if CORS_ORIGINS is set, you MUST restart for it to take effect:
- Railway → Service → Settings → **Restart**
- Or trigger a new deployment

### 4. Test CORS Directly
Open browser console on your Vercel app and run:
```javascript
fetch('https://no-colon-still-rollin-production.up.railway.app/api/health', {
  method: 'GET',
  headers: { 'Content-Type': 'application/json' }
})
.then(r => r.json())
.then(console.log)
.catch(console.error)
```

### 5. Check Network Tab
In browser DevTools → Network tab:
- Look for the failed request
- Check if it's being blocked by CORS
- Check response headers - should have `Access-Control-Allow-Origin: *`

### 6. Verify Vercel Environment Variable
In Vercel → Your Project → Settings → Environment Variables:
- Confirm `VITE_API_URL` is set to: `https://no-colon-still-rollin-production.up.railway.app`
- Or just `/api` if using relative paths

### Most Common Issue
**Railway service needs to be RESTARTED after setting CORS_ORIGINS!**
The environment variable change won't take effect until the service restarts.
