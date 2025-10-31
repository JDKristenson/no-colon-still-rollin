# Get Your Connection String - Direct Link Method

## EASIEST WAY:

**Just click this link - it goes straight to where you need to be:**

https://supabase.com/dashboard/project/wpyntnmjncdizglqedyl/settings/database

That link should take you DIRECTLY to the Database settings page with the connection string.

---

## What You'll See:

1. A page titled "Database Settings"
2. Scroll down past the database info
3. Look for a section called **"Connection string"**
4. You'll see tabs: `URI` | `JDBC` | `Connection pooling`
5. **Click "Connection pooling"**
6. In the dropdown, select **"Transaction"**
7. **Copy the entire string** - it's the long one in the text box

It will look like:
```
postgresql://postgres.wpyntnmjncdizglqedyl:[PASSWORD]@aws-0-us-east-1.pooler.supabase.com:6543/postgres
```

---

## If The Link Doesn't Work:

1. Go to: https://supabase.com/dashboard
2. Click on your project (should show `wpyntnmjncdizglqedyl` in URL)
3. Look at the **LEFT SIDEBAR** (vertical menu on left side)
4. Scroll to bottom of sidebar, find **Settings** (⚙️ icon)
5. Click Settings → Click **"Database"**
6. Scroll down → Find "Connection string" section
7. Click "Connection pooling" tab → Copy the URI

---

## Once You Have It:

Just paste it here or run:
```bash
# I'll set everything up for you
./setup.sh
```

**Or if you want me to do it all for you, just paste the connection string and I'll handle the rest.**

