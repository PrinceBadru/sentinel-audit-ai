import os
from pydantic import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "SentinelAudit-AI"
    APP_VERSION: str = "1.0.0"
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    
    # Free-tier Groq API for Llama 3.3 70B & Qwen 2.5 72B
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    GROQ_MODEL: str = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
    GROQ_BASE_URL: str = os.getenv("GROQ_BASE_URL", "https://api.groq.com/openai/v1")
    
    # Audit threshold configs
    FAIL_ON_CRITICAL: bool = True
    MAX_FILE_SIZE_BYTES: int = 500_000  # 500KB per file

    class Config:
        env_file = ".env"

settings = Settings()
