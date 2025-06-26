# app/schemas/user.py

from typing import Optional, List

from pydantic import BaseModel, EmailStr, ConfigDict

# Импортируем схему Capsule, чтобы использовать ее для типизации
# в схеме User. Это безопасно, так как схема Capsule не ссылается
# обратно на полную схему User, что предотвращает циклические импорты.
from .capsule import Capsule


# --- Базовая схема с общими полями ---
# Содержит поля, которые являются общими для всех схем пользователя.
class UserBase(BaseModel):
    email: EmailStr


# --- Схема для создания нового пользователя ---
# Наследуется от UserBase и добавляет поле для пароля,
# которое необходимо только при регистрации.
class UserCreate(UserBase):
    password: str


# --- Схема для обновления пользователя ---
# В данный момент не используется, но может быть полезна в будущем.
# Все поля являются опциональными.
class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    password: Optional[str] = None


# --- Основная схема для отображения пользователя ---
# Эта схема используется при возврате данных из API.
# Она НЕ содержит 'hashed_password' из соображений безопасности.
class User(UserBase):
    id: int
    is_active: bool
    capsules: List[Capsule] = []

    # Конфигурация для работы с моделями SQLAlchemy.
    # from_attributes=True позволяет Pydantic читать данные
    # напрямую из атрибутов ORM-объекта.
    model_config = ConfigDict(from_attributes=True)
