# app/api/v1/endpoints/auth.py

from datetime import timedelta
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app import schemas, models, crud
from app.api import deps
from app.core import security
from app.core.config import settings

# Создаем новый роутер для эндпоинтов аутентификации
router = APIRouter()


@router.post("/signup", response_model=schemas.User)
def create_user(
    *,
    db: Session = Depends(deps.get_db),
    user_in: schemas.UserCreate,
) -> Any:
    """
    Создание нового пользователя (регистрация).
    """
    # Проверяем, не занят ли уже такой email
    user = crud.user.get_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Пользователь с таким email уже существует.",
        )
    # Создаем пользователя в базе данных
    user = crud.user.create(db, obj_in=user_in)
    return user


@router.post("/login/access-token", response_model=schemas.Token)
def login_for_access_token(
    db: Session = Depends(deps.get_db),
    form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """
    Получение Access Token для пользователя (вход в систему).
    """
    # Аутентифицируем пользователя по email и паролю
    user = crud.user.authenticate(
        db, email=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный email или пароль.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    # Создаем access token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        user.id, expires_delta=access_token_expires
    )
    return {
        "access_token": access_token,
        "token_type": "bearer",
    }


@router.get("/me", response_model=schemas.User)
def read_current_user(
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Получение данных о текущем авторизованном пользователе.
    """
    return current_user
