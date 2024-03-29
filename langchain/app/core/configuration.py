import secrets
from typing import Any, Dict, List, Optional, Union
from pathlib import Path
from pydantic import AnyHttpUrl, BaseSettings, EmailStr, HttpUrl, PostgresDsn, validator
import os
from pathlib import Path

from dotenv import load_dotenv

dotenv_path = Path(__file__).resolve().parent.parent.parent / "env/backend.env"

load_dotenv(dotenv_path)


class Settings(BaseSettings):
    HOST: str = "127.0.0.1"
    PORT: int = 8000
    RELOAD: bool = False
    API_V1_STR: str = os.environ.get("API_V1_STR")
    SOCKET_V1_STR: str = "/socket/v1"
    SECRET_KEY: str = os.environ.get("SECRET_KEY")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 90
    REFRESH_TOKEN_EXPIRE_MINUTES: int = ACCESS_TOKEN_EXPIRE_MINUTES * 60
    BACKEND_CORS_ORIGINS: Union[List[str], str] = os.environ.get("BACKEND_CORS_ORIGINS")

    @validator("BACKEND_CORS_ORIGINS", pre=True, always=True)
    def assemble_cors_origins(cls, value: Union[List[str], str]) -> List[str]:
        if isinstance(value, str):
            return [url.strip() for url in value.split(",")]

        if isinstance(value, list):
            return value

        raise ValueError("invalid backend cors origin")

    PROJECT_NAME: str = os.environ.get("PROJECT_NAME")
    POSTGRES_HOST: str = os.environ.get("POSTGRES_HOST")
    POSTGRES_USER: str = os.environ.get("POSTGRES_USER")
    POSTGRES_PASSWORD: str = os.environ.get("POSTGRES_PASSWORD")
    POSTGRES_DB: str = os.environ.get("POSTGRES_DB")
    POSTGRES_PORT: str = os.environ.get("POSTGRES_PORT")
    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = None

    FROM_EMAIL: str = os.environ.get("FROM_EMAIL")
    SENDGRID_API_KEY: str = os.environ.get("SENDGRID_API_KEY")

    @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v

        return PostgresDsn.build(
            scheme="postgresql",
            user=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_HOST"),
            port=values.get("POSTGRES_PORT"),
            path=f"/{values.get('POSTGRES_DB') or ''}",
        )

    FIRST_SUPERUSER_FIRST_NAME = os.environ.get("FIRST_SUPERUSER_FIRST_NAME")
    FIRST_SUPERUSER_LAST_NAME = os.environ.get("FIRST_SUPERUSER_LAST_NAME")
    FIRST_SUPERUSER_EMAIL = os.environ.get("FIRST_SUPERUSER_EMAIL")
    FIRST_SUPERUSER_PASSWORD = os.environ.get("FIRST_SUPERUSER_PASSWORD")

    REDIS_HOST_URL = os.environ.get("REDIS_HOST_URL", None)

    CELERY_BROKER_URL = os.environ.get("CELERY_BROKER_URL", None)

    SENTRY_DSN = os.environ.get("SENTRY_DSN", None)

    class Config:
        case_sensitive = True


settings = Settings()
