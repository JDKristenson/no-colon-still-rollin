from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from app.core.config import settings

# Configure passlib to truncate passwords automatically (bcrypt limit is 72 bytes)
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
    bcrypt__max_password_length=72  # Set max length for bcrypt
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
        password = password_bytes[:72].decode('utf-8', errors='ignore')
    
    try:
        return pwd_context.hash(password)
    except ValueError as e:
        # If passlib still complains, truncate more aggressively
        if "cannot be longer than 72 bytes" in str(e):
            # Fallback: truncate to safe length
            safe_password = password_bytes[:70].decode('utf-8', errors='ignore')
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

