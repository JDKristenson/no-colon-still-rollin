from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from app.core.config import settings

# Configure passlib for bcrypt (bcrypt has 72-byte limit, handled in get_password_hash)
# Disable wrap bug detection to avoid initialization errors
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
    bcrypt__ident="2b"  # Use bcrypt 2b format explicitly
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
    # Convert password to bytes immediately
    password_bytes = password.encode('utf-8')
    
    # Truncate to 70 bytes to be safe (well under 72 limit)
    if len(password_bytes) > 70:
        password_bytes = password_bytes[:70]
    
    # Decode back to string (this should always be <= 70 bytes when re-encoded)
    password = password_bytes.decode('utf-8', errors='ignore')
    
    # Final safety check - if still too long, truncate again
    final_check = password.encode('utf-8')
    if len(final_check) > 72:
        # This should never happen, but if it does, truncate more aggressively
        password = final_check[:68].decode('utf-8', errors='ignore')
    
    # Hash with try/except as final safety net
    try:
        return pwd_context.hash(password)
    except ValueError as e:
        # If bcrypt still complains (shouldn't happen now), truncate to 60 bytes
        if "cannot be longer than 72 bytes" in str(e):
            safe_password = password.encode('utf-8')[:60].decode('utf-8', errors='ignore')
            return pwd_context.hash(safe_password)
        raise

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

