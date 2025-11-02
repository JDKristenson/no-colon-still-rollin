import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.core.config import settings

logger = logging.getLogger(__name__)

def send_verification_email(email: str, name: str, verification_token: str) -> bool:
    """
    Send email verification email to user.
    Returns True if successful, False otherwise.
    """
    # Skip sending if SMTP is not configured
    if not settings.SMTP_USER or not settings.SMTP_PASSWORD:
        logger.warning(f"SMTP not configured - skipping email verification for {email}")
        logger.warning(f"Verification token (for testing): {verification_token}")
        return False
    
    try:
        # Create message
        msg = MIMEMultipart("alternative")
        msg["Subject"] = "Verify Your Email - No Colon, Still Rollin'"
        msg["From"] = f"{settings.SMTP_FROM_NAME} <{settings.SMTP_FROM_EMAIL}>"
        msg["To"] = email
        
        # Verification URL
        verification_url = f"{settings.FRONTEND_URL}/verify-email?token={verification_token}"
        
        # Create email body
        text_content = f"""
Hi {name},

Welcome to No Colon, Still Rollin'!

Please verify your email address by clicking the link below:

{verification_url}

If you didn't create an account, you can safely ignore this email.

Stay strong,
The No Colon, Still Rollin' Team
"""
        
        html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <style>
        body {{
            font-family: Arial, sans-serif;
            line-height: 1.6;
            color: #333;
        }}
        .container {{
            max-width: 600px;
            margin: 0 auto;
            padding: 20px;
        }}
        .button {{
            display: inline-block;
            padding: 12px 30px;
            background-color: #2563eb;
            color: white;
            text-decoration: none;
            border-radius: 5px;
            margin: 20px 0;
        }}
        .button:hover {{
            background-color: #1d4ed8;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h2>Welcome to No Colon, Still Rollin'!</h2>
        <p>Hi {name},</p>
        <p>Thank you for joining our community. Please verify your email address by clicking the button below:</p>
        <p>
            <a href="{verification_url}" class="button">Verify Email Address</a>
        </p>
        <p>Or copy and paste this link into your browser:</p>
        <p style="word-break: break-all; color: #666;">{verification_url}</p>
        <p>If you didn't create an account, you can safely ignore this email.</p>
        <p>Stay strong,<br>The No Colon, Still Rollin' Team</p>
    </div>
</body>
</html>
"""
        
        # Add parts to message
        part1 = MIMEText(text_content, "plain")
        part2 = MIMEText(html_content, "html")
        msg.attach(part1)
        msg.attach(part2)
        
        # Send email
        with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
            server.starttls()
            server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
            server.send_message(msg)
        
        logger.info(f"Verification email sent to {email}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to send verification email to {email}: {str(e)}", exc_info=True)
        return False

