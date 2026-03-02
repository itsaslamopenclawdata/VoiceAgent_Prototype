"""
RepCon Voice Agent - Core Application Configuration
"""
from pydantic_settings import BaseSettings
from typing import Optional
import os


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # App
    APP_NAME: str = "RepCon Voice Agent"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    
    # Database
    DATABASE_URL: str = "postgresql+asyncpg://repcon:repcon123@localhost:5432/repcon"
    DATABASE_ECHO: bool = False
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379"
    
    # JWT Auth
    SECRET_KEY: str = "your-secret-key-change-in-production"
    JWT_SECRET: str = "your-jwt-secret-change-in-production"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Ollama
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    OLLAMA_MODEL: str = "llama3.2"
    
    # Twilio
    TWILIO_ACCOUNT_SID: Optional[str] = None
    TWILIO_AUTH_TOKEN: Optional[str] = None
    TWILIO_PHONE_NUMBER: Optional[str] = None
    
    # Google Sheets
    GOOGLE_SERVICE_ACCOUNT_JSON: Optional[str] = None
    GOOGLE_SHEETS_ID: Optional[str] = None
    
    # CORS
    CORS_ORIGINS: list = ["http://localhost:3000", "http://localhost:8000"]
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
