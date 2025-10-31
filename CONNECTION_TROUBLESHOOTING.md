# Connection String Troubleshooting

## Current Issues

1. **Pooler connection**: "Tenant or user not found"
2. **Direct connection**: Hostname not resolving

## Connection String Formats to Try

### Format 1: Transaction Pooler (Serverless)
```
postgresql://postgres.[PROJECT-REF]:[PASSWORD]@aws-0-[REGION].pooler.supabase.com:6543/postgres
```

### Format 2: Direct Connection
```
postgresql://postgres:[PASSWORD]@db.[PROJECT-REF].supabase.co:5432/postgres
```

### Format 3: Session Pooler
```
postgresql://postgres.[PROJECT-REF]:[PASSWORD]@aws-0-[REGION].pooler.supabase.com:5432/postgres
```

## Your Current Values

- **Project Ref**: `wpyntnmjncdizglqedyl`
- **Password**: `2022Freshstart`
- **Region**: `us-east-1`

## Next Steps

1. **Verify in Supabase Dashboard**:
   - Go to: https://supabase.com/dashboard/project/wpyntnmjncdizglqedyl
   - Settings → Database
   - Look for "Connection string" - it should show the exact format
   - If it's not visible, check if there's a "Connect" button or tab

2. **Try SQL Editor Method**:
   - Go to SQL Editor in Supabase
   - Run a query - the connection info might appear in browser dev tools or the page URL

3. **Check Project Status**:
   - Make sure the Supabase project is active and not paused
   - Check if there are any IP restrictions

4. **Alternative: Get from Supabase CLI**:
   ```bash
   npm install -g supabase
   supabase login
   supabase link --project-ref wpyntnmjncdizglqedyl
   supabase status
   ```

## If Password is Wrong

If none of the connection strings work, the password might be incorrect. You can:
1. Reset database password in Supabase Dashboard
2. Settings → Database → Reset Password

Then try again with the new password.

