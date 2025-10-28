# PubMed API Key Setup Guide

The system uses NCBI's E-utilities API to fetch anti-cancer food research from PubMed. You'll need a free API key for best performance.

---

## Why You Need an API Key

**Without API key**: 3 requests per second
**With API key**: 10 requests per second

For updating the research database with dozens of studies, the API key makes it much faster and more reliable.

---

## Step-by-Step Setup

### 1. Create NCBI Account

Go to: **https://www.ncbi.nlm.nih.gov/account/**

Click **"Register for an NCBI account"**

### 2. Fill Out Registration

- **Email**: Use kristenson@gmail.com (or your preferred email)
- **Username**: Choose any username
- **Password**: Create a secure password
- **First Name**: JD
- **Last Name**: Kristenson

Click **"Register"**

### 3. Verify Email

- Check your email for verification link
- Click the verification link
- Log into your new NCBI account

### 4. Navigate to API Key Settings

Once logged in:

1. Click your **username** in the top right
2. Select **"Account settings"**
3. In the left sidebar, click **"API Key Management"**

### 5. Generate API Key

1. Click **"Create an API Key"**
2. Your new API key will appear (long string of letters and numbers)
3. **Copy the API key** immediately

**IMPORTANT**: Save this key somewhere secure. You can regenerate it if lost, but it's easier to save it now.

### 6. Add to Environment File

Open the file: `.env`

Update this line:
```bash
NCBI_API_KEY=your_key_here
```

Replace `your_key_here` with your actual API key.

**Example:**
```bash
NCBI_API_KEY=a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8
```

Save the file.

### 7. Test the API Key

Run:
```bash
cd "/Users/JDKristenson/Desktop/No Colon Still Rollin"
python3 src/main.py update-research --max 5
```

If the API key works, you'll see:
```
🔬 Updating research from PubMed...
🔍 Searching PubMed: cancer AND (ginger OR gingerol)
  Found 5 articles
  ✅ Added: [Article title]...
```

If there's an error with the API key, you'll see an error message.

---

## Troubleshooting

### "API key is invalid"
- Double-check you copied the entire key
- Make sure there are no extra spaces
- Regenerate the key in NCBI account settings

### "HTTP 429: Too many requests"
- You're hitting rate limits
- Add your API key (see above)
- Or reduce `--max` parameter

### "Biopython not installed"
```bash
pip install biopython
```

---

## API Key Security

✅ **Safe to store in `.env`** (this file is in `.gitignore`, won't be committed to git)

❌ **Never commit API keys to GitHub**

❌ **Never share API keys publicly**

✅ **API keys are free and can be regenerated** if compromised

---

## Additional NCBI Resources

- **E-utilities Documentation**: https://www.ncbi.nlm.nih.gov/books/NBK25501/
- **API Rate Limits**: https://www.ncbi.nlm.nih.gov/books/NBK25497/#chapter2.Usage_Guidelines_and_Requiremen
- **Support**: https://support.ncbi.nlm.nih.gov/

---

## For Future Reference

Your NCBI account dashboard: https://www.ncbi.nlm.nih.gov/account/

You can:
- View API usage statistics
- Regenerate API keys
- Update account settings
- Access other NCBI databases

---

**That's it! Your PubMed research updater is now fully configured.** 🎉
