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
    CORS_ORIGINS: str = "http://localhost:5173,http://localhost:3000,http://localhost:5174"
    
    def get_cors_origins(self) -> List[str]:
        """Parse CORS_ORIGINS from string to list"""
        if isinstance(self.CORS_ORIGINS, str):
            return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]
        return self.CORS_ORIGINS if isinstance(self.CORS_ORIGINS, list) else []
    
    # App
    PROJECT_NAME: str = "No Colon, Still Rollin'"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()

