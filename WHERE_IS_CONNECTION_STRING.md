# Where the F*ck is the Supabase Connection String?

## Exact Location (With Screenshots in Mind)

### Option 1: Direct Link (Easiest)

Just click this link (it goes straight to the connection string page):
https://supabase.com/dashboard/project/wpyntnmjncdizglqedyl/settings/database

That should take you DIRECTLY to the Database settings page.

### Option 2: Step-by-Step Navigation

1. **Go to your project dashboard:**
   https://supabase.com/dashboard/project/wpyntnmjncdizglqedyl

2. **Look at the LEFT SIDEBAR** (not the top menu)
   - You'll see icons: Home, Database, Authentication, Storage, etc.
   - Click the **⚙️ Settings** icon (gear/cog icon) at the BOTTOM of the sidebar

3. **Settings menu opens** - Click **"Database"** (first option usually)

4. **Database Settings page** - Scroll down past all the info

5. **Find "Connection string" section**
   - It's a gray box with tabs at the top
   - Tabs say: "URI", "JDBC", "Connection pooling"

6. **Click "Connection pooling" tab**

7. **Select "Transaction" mode** (dropdown)

8. **Copy the string** - It's the long one starting with `postgresql://`

### Option 3: Use SQL Editor (Alternative)

If you can't find it the normal way:

1. Go to: https://supabase.com/dashboard/project/wpyntnmjncdizglqedyl
2. Click **"SQL Editor"** in left sidebar
3. Click **"New query"**
4. Run this query:
   ```sql
   SELECT current_database(), current_user;
   ```
5. The connection info is in the URL bar or you can use the connection string format:
   ```
   postgresql://postgres.[PROJECT-REF]:[YOUR-PASSWORD]@db.[PROJECT-REF].supabase.co:5432/postgres
   ```

### What It Should Look Like

The connection string will be something like:
```
postgresql://postgres.wpyntnmjncdizglqedyl:[YOUR-PASSWORD]@aws-0-us-east-1.pooler.supabase.com:6543/postgres
```

**For Transaction Pooler (RECOMMENDED):**
- Port: **6543**
- Host: `aws-0-[region].pooler.supabase.com`

**For Direct Connection:**
- Port: **5432**  
- Host: `db.[project-ref].supabase.co`

### Still Can't Find It?

1. **Check if you're in the right project:**
   - URL should have: `wpyntnmjncdizglqedyl`
   - If not, navigate to that project first

2. **Check your permissions:**
   - Make sure you're the project owner or have admin access
   - If not, ask the project owner for the connection string

3. **Use Supabase CLI instead:**
   ```bash
   # Install Supabase CLI
   brew install supabase/tap/supabase  # Mac
   # or
   npm install -g supabase  # Node
   
   # Login
   supabase login
   
   # Link to your project
   supabase link --project-ref wpyntnmjncdizglqedyl
   
   # Get connection string
   supabase status
   ```

### Quick Alternative: I'll Help You Build It

If you can tell me:
- Your Supabase project password (the one you set when creating the project)
- Your project region (us-east-1, eu-west-1, etc.)

I can help construct the connection string. Or just give me the password and I'll guide you through finding the region.

### Nuclear Option: Reset and Use New Project

If this is too frustrating, we can:
1. Create a NEW Supabase project just for this app
2. Get the connection string from the welcome screen (it's shown there!)
3. Use that fresh project

---

**TL;DR:**
1. Go here: https://supabase.com/dashboard/project/wpyntnmjncdizglqedyl/settings/database
2. Scroll to "Connection string"
3. Click "Connection pooling" tab
4. Copy the URI

**Or run:** `python find_connection_string.py` and I'll walk you through it interactively.

