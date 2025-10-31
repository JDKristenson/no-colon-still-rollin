# Alternative Ways to Get Supabase Connection Info

Since the connection string section isn't visible, here are other methods:

## Method 1: SQL Editor (Easiest)

1. Go to: https://supabase.com/dashboard/project/wpyntnmjncdizglqedyl
2. Click **"SQL Editor"** in left sidebar
3. Click **"New query"**
4. Run this query:
   ```sql
   SELECT 
     current_database() as database,
     current_user as user,
     inet_server_addr() as host,
     inet_server_port() as port;
   ```
5. This will show your connection details
6. Then use: `construct_connection.py` to build the full string

## Method 2: API Settings (Find Project Info)

1. Go to: https://supabase.com/dashboard/project/wpyntnmjncdizglqedyl/settings/api
2. You'll see:
   - Project URL
   - Project reference (we already have: `wpyntnmjncdizglqedyl`)
   - API keys
3. Use `construct_connection.py` with your password

## Method 3: Construct It Manually

Run this script - it will ask for your password and region:

```bash
python3 construct_connection.py
```

You'll need:
- Your Supabase database password (the one you set when creating project)
- Your project region (US East, EU West, etc.)

## Method 4: Use Supabase CLI

Install Supabase CLI:

```bash
# Mac
brew install supabase/tap/supabase

# Or via npm
npm install -g supabase
```

Then:

```bash
supabase login
supabase link --project-ref wpyntnmjncdizglqedyl
supabase status
```

This will show connection strings.

## Method 5: Check Project Settings → General

Sometimes connection info is in:
1. Settings → General
2. Look for "Connection Info" or "Database Connection"

## Method 6: Reset Password and Get Connection String

If you forgot the password:

1. Settings → Database
2. Look for "Reset Database Password" or "Change Password"
3. After reset, the new connection string might be shown

## What You Need to Know

Your connection string format:
```
postgresql://postgres.[PROJECT-REF]:[PASSWORD]@[HOST]:[PORT]/postgres
```

We know:
- Project Ref: `wpyntnmjncdizglqedyl`
- Need: Password, Region/Host

**Run `construct_connection.py` - it will ask for the missing pieces!**

