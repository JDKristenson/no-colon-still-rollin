# Email Verification Setup

## ✅ What's Been Added

Email verification has been implemented in the FastAPI backend:

1. **User Model Updates** - Added fields:
   - `email_verified` (Boolean, defaults to False)
   - `email_verification_token` (String, indexed for fast lookups)
   - `email_verification_sent_at` (DateTime)

2. **New API Endpoints**:
   - `POST /api/auth/verify-email?token=<token>` - Verify email with token
   - `POST /api/auth/resend-verification` - Resend verification email (requires auth)

3. **Email Sending** - SMTP-based email sending utility
4. **Registration Flow** - Automatically generates and sends verification token

## 🔧 Configuration Required

To enable email sending, set these environment variables in Railway:

### Option 1: Gmail (Easy for Development)

```bash
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password  # Use Gmail App Password, not regular password
SMTP_FROM_EMAIL=your-email@gmail.com
SMTP_FROM_NAME=No Colon, Still Rollin'
FRONTEND_URL=https://your-vercel-app.vercel.app
```

**Gmail Setup:**
1. Enable 2-Factor Authentication on your Google account
2. Go to: https://myaccount.google.com/apppasswords
3. Generate an "App Password" for "Mail"
4. Use that 16-character password (not your regular Gmail password)

### Option 2: SendGrid (Recommended for Production)

```bash
SMTP_HOST=smtp.sendgrid.net
SMTP_PORT=587
SMTP_USER=apikey
SMTP_PASSWORD=your-sendgrid-api-key
SMTP_FROM_EMAIL=noreply@yourdomain.com
SMTP_FROM_NAME=No Colon, Still Rollin'
FRONTEND_URL=https://your-vercel-app.vercel.app
```

### Option 3: Mailgun

```bash
SMTP_HOST=smtp.mailgun.org
SMTP_PORT=587
SMTP_USER=postmaster@your-domain.mailgun.org
SMTP_PASSWORD=your-mailgun-smtp-password
SMTP_FROM_EMAIL=noreply@yourdomain.com
SMTP_FROM_NAME=No Colon, Still Rollin'
FRONTEND_URL=https://your-vercel-app.vercel.app
```

### Option 4: AWS SES

```bash
SMTP_HOST=email-smtp.us-east-1.amazonaws.com  # Adjust region
SMTP_PORT=587
SMTP_USER=your-aws-smtp-username
SMTP_PASSWORD=your-aws-smtp-password
SMTP_FROM_EMAIL=noreply@yourdomain.com
SMTP_FROM_NAME=No Colon, Still Rollin'
FRONTEND_URL=https://your-vercel-app.vercel.app
```

## 🚀 Setup Steps

1. **Add Environment Variables in Railway:**
   - Go to: https://railway.com/project/fd467ce0-7ede-45a1-aefd-9a35d8e47026/service/be163e70-674e-4cca-bd02-c71e0d04fb07/variables
   - Add all SMTP variables and FRONTEND_URL
   - Railway will auto-restart

2. **Run Database Migration:**
   - The migration file is already created: `backend/alembic/versions/add_email_verification_fields.py`
   - Railway should run migrations automatically, or you can run manually:
     ```bash
     railway run alembic upgrade head
     ```

3. **Test:**
   - Register a new user
   - Check email for verification link
   - Click link or use the token in the API

## 📧 Email Behavior

- **Without SMTP configured:** Registration still works, but verification email is skipped (logged to console)
- **With SMTP configured:** Verification email is sent automatically on registration
- **Email includes:** HTML and plain text versions with verification link

## 🔗 Verification Link Format

```
https://your-vercel-app.vercel.app/verify-email?token=<verification-token>
```

The token is a JWT that expires in 24 hours.

## 🔄 Frontend Integration Needed

You'll need to create a frontend page to handle email verification:

1. **Create `/verify-email` route** that:
   - Extracts token from URL query params
   - Calls `POST /api/auth/verify-email?token=<token>`
   - Shows success/error message

2. **Update registration flow** to show message like:
   "Registration successful! Please check your email to verify your account."

3. **Add resend button** (optional) that calls `/api/auth/resend-verification`

## 🛠️ Development Mode

If SMTP is not configured, the system logs the verification token to the console/logs instead of sending email. This allows development without email setup.

Check Railway logs to see verification tokens during development.

