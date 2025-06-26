# app/api/v1/deps.py

from typing import Generator

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from pydantic import ValidationError
from sqlalchemy.orm import Session

from app import models, schemas, crud
from app.core import security
from app.core.config import settings
from app.db.session import SessionLocal

# Схема аутентификации OAuth2.
# Указывает, что токен должен быть получен с эндпоинта /api/v1/auth/login/access-token
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/auth/login/access-token"
)

def get_db() -> Generator:
    """
    Зависимость для получения сессии базы данных.
    Эта функция создает новую сессию для каждого запроса и закрывает ее после завершения.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
) -> models.User:
    """
    Зависимость для получения текущего пользователя на основе JWT токена.
    """
    try:
        # Декодируем JWT токен
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        # Валидируем данные из токена с помощью Pydantic схемы
        # Используем 'sub' (subject) как стандартное поле для ID пользователя в JWT
        token_data = schemas.TokenData(id=int(payload.get("sub")))
    except (JWTError, ValidationError, TypeError):
        # Если токен невалидный или данные в нем некорректны, выбрасываем исключение
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Не удалось проверить учетные данные",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Получаем пользователя из базы данных по ID из токена
    user = crud.user.get(db, id=token_data.id)
    if not user:
        # Если пользователь не найден, выбрасываем исключение
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Пользователь не найден")
    return user


def get_current_active_user(
    current_user: models.User = Depends(get_current_user),
) -> models.User:
    """
    Зависимость для получения текущего активного пользователя.
    Проверяет, что пользователь, полученный из токена, активен.
    """
    if not crud.user.is_active(current_user):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Неактивный пользователь")
    return current_user
