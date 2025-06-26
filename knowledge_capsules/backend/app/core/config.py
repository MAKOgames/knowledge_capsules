# app/core/config.py

from typing import List, Union

from pydantic import AnyHttpUrl, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """
    Класс для хранения всех настроек приложения.
    Настройки загружаются из переменных окружения и .env файла.
    """
    # --- Основные настройки проекта ---
    PROJECT_NAME: str = "Knowledge Capsules"
    API_V1_STR: str = "/api/v1"

    # --- Настройки безопасности (JWT) ---
    SECRET_KEY: str
    # Алгоритм для подписи JWT
    ALGORITHM: str = "HS256"
    # Время жизни Access Token в минутах
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 дней

    # --- Настройки базы данных (PostgreSQL) ---
    # URL для подключения к базе данных
    DATABASE_URL: str

    # --- Настройки CORS ---
    # Список источников, которым разрешен доступ к API
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    # Валидатор для BACKEND_CORS_ORIGINS
    @field_validator("BACKEND_CORS_ORIGINS", mode='before')
    @classmethod
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    # --- Настройки Email сервиса (SendGrid) ---
    SENDGRID_API_KEY: str
    EMAILS_FROM_EMAIL: str

    # --- Настройки Celery (Redis) ---
    CELERY_BROKER_URL: str
    CELERY_RESULT_BACKEND: str
    
    # --- Указываем, что нужно читать переменные из .env файла ---
    model_config = SettingsConfigDict(case_sensitive=True, env_file=".env")


# Создаем единственный экземпляр настроек,
# который будет импортироваться в другие модули
settings = Settings()
