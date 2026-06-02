from typing import List, Union
from pydantic import AnyHttpUrl, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "TERRAVA Ag-OS Backend"
    API_V1_STR: str = "/api/v1"
    
    # Security Configurations
    JWT_SECRET_KEY: str = "7a8c4bd2d6b38c230e7f7b183610deefb5a195e86976a26df0167c525f231e3d"
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440  # 24 Hours
    
    # Firebase Configurations
    FIREBASE_PROJECT_ID: str = "terrava-farm"
    FIREBASE_STORAGE_BUCKET: str = "terrava-farm.firebasestorage.app"
    FIREBASE_DATABASE_URL: str = "https://terrava-farm-default-rtdb.firebaseio.com"
    FIREBASE_CREDENTIALS_PATH: str = ""  # If empty, uses Application Default Credentials
    
    # External API Integrations
    OPENWEATHER_API_KEY: str = ""
    HUGGINGFACE_API_KEY: str = ""
    HF_TOKEN: str = ""  # Alternative env var name for HuggingFace token

    @property
    def hf_token(self) -> str:
        """Return the active HuggingFace token, preferring HF_TOKEN over HUGGINGFACE_API_KEY."""
        if self.HF_TOKEN and not self.HF_TOKEN.startswith("demo_"):
            return self.HF_TOKEN
        if self.HUGGINGFACE_API_KEY and not self.HUGGINGFACE_API_KEY.startswith("demo_"):
            return self.HUGGINGFACE_API_KEY
        return ""

    # CORS settings
    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:8000",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:8000",
        "https://terrava-farm.web.app",
        "https://terrava-farm.firebaseapp.com"
    ]

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )


settings = Settings()
