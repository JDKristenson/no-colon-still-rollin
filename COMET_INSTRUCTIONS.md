# Instructions for Comet AI Browser to Find Supabase Connection String

## Mission
Navigate to your Supabase project dashboard and locate the database connection string.

## Step-by-Step Instructions for Comet

### Step 1: Navigate to Supabase Dashboard
1. **Go to**: `https://supabase.com/dashboard/project/wpyntnmjncdizglqedyl`
   - Direct URL to your project
   - Alternative: Go to `https://supabase.com/dashboard` and select the project with ref `wpyntnmjncdizglqedyl`

### Step 2: Access Database Settings
1. **Look for Settings in the left sidebar**
   - Usually represented by a gear/cog icon (⚙️)
   - Located at the bottom of the sidebar menu
   - Click on it

2. **Click on "Database"**
   - Should be the first or second option under Settings
   - Alternatively, look for "Database Settings" or "Database Configuration"

### Step 3: Find Connection String Section
1. **Scroll down the Database Settings page**
   - Look for a section titled:
     - "Connection string"
     - "Connection info"
     - "Database URL"
     - "Connection pooling"
     - "Database credentials"

2. **Look for tabs or buttons**:
   - Tabs might say: "URI", "JDBC", "Connection pooling"
   - Buttons might say: "Connect", "Show connection string", "Reveal"
   - Click on these if visible

3. **Check for a gray box or code block**
   - Connection strings are often displayed in a gray/colored box
   - May have a "Copy" button next to it
   - Should start with `postgresql://`

### Step 4: Try Alternative Locations if Not Found

**Option A: Top Bar "Connect" Button**
1. Look at the top of the page (toolbar/header area)
2. Look for a button labeled "Connect" or "Connect to Database"
3. Click it if found

**Option B: SQL Editor Method**
1. Click "SQL Editor" in the left sidebar
2. Look for connection info in:
   - The URL bar (check for connection parameters)
   - A connection panel on the left
   - Settings/gear icon within SQL Editor

**Option C: Project Settings → General**
1. Go back to Settings → General
2. Look for "Connection Info" or "Database Connection" section

**Option D: API Settings Page**
1. Settings → API
2. Sometimes connection info is shown here alongside API keys

### Step 5: What to Look For

The connection string should look like one of these formats:

**Transaction Pooler (recommended for serverless):**
```
postgresql://postgres.[PROJECT-REF]:[PASSWORD]@aws-0-[REGION].pooler.supabase.com:6543/postgres
```

**Direct Connection:**
```
postgresql://postgres:[PASSWORD]@db.[PROJECT-REF].supabase.co:5432/postgres
```

**Session Pooler:**
```
postgresql://postgres.[PROJECT-REF]:[PASSWORD]@aws-0-[REGION].pooler.supabase.com:5432/postgres
```

### Step 6: Copy the Connection String

Once found:
1. Click the "Copy" button if available
2. Or select all text and copy (Cmd+C / Ctrl+C)
3. The full connection string will include your password

### Step 7: Report Back

Comet should provide:
1. The **complete connection string** (including password)
2. Which **format** it is (Transaction Pooler, Direct, or Session)
3. Which **tab/section** it was found in
4. **Screenshot** if possible (for verification)

## What to Do If Comet Can't Find It

### Alternative: Use Browser Dev Tools
1. Open browser developer tools (F12 or Cmd+Option+I)
2. Go to Network tab
3. Navigate to Database Settings page
4. Look for API calls containing "connection" or "database"
5. Check response data for connection strings

### Alternative: Check Page Source
1. Right-click on Database Settings page → "View Page Source"
2. Search (Cmd+F / Ctrl+F) for "postgresql://"
3. The connection string might be embedded in the page source

## Expected Project Information

- **Project Reference**: `wpyntnmjncdizglqedyl`
- **Region**: US East (likely `us-east-1`)
- **Password**: `2022Freshstart`

## Quick Command for Comet

```
Navigate to https://supabase.com/dashboard/project/wpyntnmjncdizglqedyl/settings/database

Look for a section called "Connection string" 

Find and copy the connection string that starts with "postgresql://"

Report the full connection string including the password portion.
```

## Visual Cues for Comet

- Look for **code blocks** or **monospace text** (usually gray boxes)
- Look for **"Copy" icons** (usually a square with lines)
- Look for **tabs** at the top of sections (URI, JDBC, etc.)
- Look for **dropdowns** that might say "Transaction" or "Session"
- Connection strings are usually **long** (100+ characters)
- They contain **your project ref**: `wpyntnmjncdizglqedyl`

---

**Once Comet finds it, paste the connection string here and I'll update the setup automatically!**

