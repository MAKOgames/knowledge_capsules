# app/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Импортируем роутеры из соответствующих модулей
from app.api.v1.endpoints import auth, capsules
from app.core.config import settings

# --- Инициализация FastAPI приложения ---
# Задаем название и версию API, которые будут отображаться в документации
app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# --- Настройка CORS (Cross-Origin Resource Sharing) ---
# Это необходимо, чтобы ваше frontend-приложение (например, на localhost:3000)
# могло отправлять запросы к этому backend-серверу (например, на localhost:8000).
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],  # Разрешаем все методы (GET, POST, etc.)
        allow_headers=["*"],  # Разрешаем все заголовки
    )

# --- Подключение роутеров API ---
# Включаем роутеры для аутентификации и капсул,
# задавая им префиксы для версионирования API.
app.include_router(auth.router, prefix=f"{settings.API_V1_STR}/auth", tags=["Auth"])
app.include_router(capsules.router, prefix=f"{settings.API_V1_STR}/capsules", tags=["Capsules"])


# --- Корневой эндпоинт ---
# Простой эндпоинт для проверки работоспособности API.
@app.get("/", tags=["Root"])
async def root():
    """
    Приветственный эндпоинт.
    """
    return {"message": "Welcome to Knowledge Capsules API"}

