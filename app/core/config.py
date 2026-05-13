from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    # PROJECT
    PROJECT_NAME: str = "FastAPI Project"
    VERSION: str = "1.0.0"
    DESCRIPTION: str = "A production-ready FastAPI application"
    API_V1_STR: str = "/api/v1"
    DEBUG: bool = False

    # SECURITY
    SECRET_KEY: str = "change-me-in-production"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    ALGORITHM: str = "HS256"

    # DATABASE
    DATABASE_URL: str = "sqlite+aiosqlite:///./dev.db"

    # CORS
    ALLOWED_ORIGINS: List[str] = ["https://localhost:3000"]
    model_config = {"env_file": ".env", "case_sensitive": True}

settings = Settings()