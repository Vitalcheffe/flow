"""
FLOW configuration using pydantic-settings.
All config comes from environment variables or .env file.
"""

from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    APP_NAME: str = "FLOW"
    APP_ENV: str = "development"
    DEBUG: bool = True
    LOG_LEVEL: str = "info"

    HOST: str = "0.0.0.0"
    PORT: int = 8000

    DATABASE_URL: str = "sqlite:///./flow.db"

    CUDA_VISIBLE_DEVICES: str = "0"
    USE_GPU: bool = True

    NEURAL_MODEL_DIR: str = "./models"
    DEFAULT_SOLVER: str = "fea_classic"

    CORS_ORIGINS: List[str] = ["http://localhost:5173", "http://localhost:3000"]

    UPLOAD_DIR: str = "./uploads"
    RESULTS_DIR: str = "./results"
    MAX_UPLOAD_SIZE_MB: int = 100

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
