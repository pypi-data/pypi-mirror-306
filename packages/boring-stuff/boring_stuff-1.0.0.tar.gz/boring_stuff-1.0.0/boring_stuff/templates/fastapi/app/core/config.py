import os
from pydantic import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "FastAPI Project"
    DB_URL: str = os.getenv("DATABASE_URL", "sqlite:///./test.db")

settings = Settings()
