from typing import List, Optional
from pydantic_settings import BaseSettings
from pydantic import field_validator
import os
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    # API Configuration
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "eWash API"
    DEBUG: bool = True
    
    # Supabase Configuration
    SUPABASE_URL: str = os.getenv("SUPABASE_URL", "https://ajqkrulblcfjvbfobiph.supabase.co")
    SUPABASE_KEY: str = os.getenv("SUPABASE_KEY", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImFqcWtydWxibGNmanZiZm9iaXBoIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDg0ODExNjgsImV4cCI6MjA2NDA1NzE2OH0.24mS9d2HN-1tTX6ZVN1InYW0d-WtNLFX1CNEmgzy1zA")
    SUPABASE_SERVICE_KEY: Optional[str] = os.getenv("SUPABASE_SERVICE_KEY")
    
    # Database Configuration - Using Transaction Pooler (port 6543) for better compatibility
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://postgres.ajqkrulblcfjvbfobiph:mancos2024*@aws-0-us-east-2.pooler.supabase.com:6543/postgres")
    
    # JWT Configuration
    SECRET_KEY: str = os.getenv("SECRET_KEY", "eWash-super-secret-key-2024-change-in-production")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # CORS Configuration - Allow frontend origins
    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000", 
        "http://localhost:8000",
        "http://127.0.0.1:8000"
    ]
    
    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v):
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)
    
    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings() 