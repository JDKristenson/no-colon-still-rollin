from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    # Database
    # Default to Supabase format, can be overridden by environment variable
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/nocolon"
    
    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days
    
    # CORS - can be comma-separated string or list
    # Default includes common Vercel patterns
    CORS_ORIGINS: str = "http://localhost:5173,http://localhost:3000,http://localhost:5174,https://*.vercel.app"
    
    def get_cors_origins(self) -> List[str]:
        """Parse CORS_ORIGINS from string to list"""
        if isinstance(self.CORS_ORIGINS, str):
            # If CORS_ORIGINS is set to "*", allow all origins (for development)
            if self.CORS_ORIGINS.strip() == "*":
                return ["*"]
            origins = [origin.strip() for origin in self.CORS_ORIGINS.split(",")]
            # Check if any origin contains wildcard or "vercel.app"
            # If so, allow all origins for easier setup
            if any("*" in origin or "vercel.app" in origin for origin in origins):
                # Temporary: allow all origins if vercel.app pattern detected
                # User should set explicit URL in Railway for production
                return ["*"]
            return origins
        if isinstance(self.CORS_ORIGINS, list):
            if "*" in self.CORS_ORIGINS or any("*" in str(o) for o in self.CORS_ORIGINS):
                return ["*"]
            return self.CORS_ORIGINS
        return []
    
    # App
    PROJECT_NAME: str = "No Colon, Still Rollin'"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()

