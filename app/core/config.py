from pydantic_settings import BaseSettings
from pathlib import Path


class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str

    ALGORITHM: str = "HS256"
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    ALLOWED_DOMAINS: list[str] = ["bankprotect.com", "company.org"]

    OLLAMA_BASE_URL: str = "http://localhost:11434"
    OLLAMA_MODEL: str = "llama3"

    class Config:
        env_file = Path(__file__).resolve().parent.parent.parent / ".env"


settings = Settings()