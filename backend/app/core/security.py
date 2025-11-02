from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from app.core.config import settings

# Configure passlib for bcrypt (bcrypt has 72-byte limit, handled in get_password_hash)
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    # Truncate password before verification to match hashing behavior
    password_bytes = plain_password.encode('utf-8')
    if len(password_bytes) > 72:
        plain_password = password_bytes[:72].decode('utf-8', errors='ignore')
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """
    Hash a password using bcrypt.
    Bcrypt has a 72-byte limit, so we truncate longer passwords.
    This is safe because bcrypt truncates at 72 bytes anyway.
    """
    # Convert password to bytes to check length
    password_bytes = password.encode('utf-8')
    if len(password_bytes) > 72:
        # Truncate to 72 bytes (not characters) - decode back to string
        # We truncate to 71 bytes to be safe, then decode
        truncated_bytes = password_bytes[:71]
        password = truncated_bytes.decode('utf-8', errors='ignore')
        # Re-encode to verify it's under 72 bytes
        if len(password.encode('utf-8')) > 72:
            # If still too long, truncate more aggressively
            password = password_bytes[:70].decode('utf-8', errors='ignore')
    
    # Double-check before hashing
    final_bytes = password.encode('utf-8')
    if len(final_bytes) > 72:
        password = final_bytes[:71].decode('utf-8', errors='ignore')
    
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError:
        return None

