from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "ContextForge AI"
    API_V1_STR: str = "/api/v1"
    
    # SECURITY
    SECRET_KEY: str = "your_super_secret_key_for_jwt_2026"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days
    ALGORITHM: str = "HS256"
    ENCRYPTION_KEY: str = "T1x3L4y5M6n7O8p9Q0r1S2t3U4v5W6x7Y8z9A0b1C2d="
    
    # DATABASE
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = ""
    POSTGRES_DB: str = "codeforge"
    POSTGRES_PORT: int = 5433
    
    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
    
    # REDIS
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # DATAHUB
    DATAHUB_GMS_URL: str = "http://localhost:8080"
    DATAHUB_TOKEN: Optional[str] = None
    
    # LLM KEYS
    OPENAI_API_KEY: Optional[str] = None
    GROQ_API_KEY: Optional[str] = None
    OPENROUTER_API_KEY: Optional[str] = None
    GEMINI_API_KEY: Optional[str] = None

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", case_sensitive=True, extra="ignore")

settings = Settings()
