# app/schemas/capsule.py

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, HttpUrl, ConfigDict


# --- Базовая схема с общими полями ---
# Содержит поля, которые есть во всех других схемах капсул.
class CapsuleBase(BaseModel):
    title: Optional[str] = None
    content: str
    source_url: Optional[HttpUrl] = None
    send_at: datetime


# --- Схема для создания новой капсулы ---
# Используется при получении данных от клиента для создания объекта.
class CapsuleCreate(CapsuleBase):
    pass


# --- Схема для обновления капсулы ---
# Все поля опциональны, чтобы клиент мог обновлять только нужные ему данные.
class CapsuleUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    source_url: Optional[HttpUrl] = None
    send_at: Optional[datetime] = None


# --- Основная схема для отображения капсулы ---
# Используется при возврате данных клиенту из API.
# Включает поля, которые генерируются базой данных (id, owner_id, etc.).
class Capsule(CapsuleBase):
    id: int
    owner_id: int
    created_at: datetime
    is_sent: bool

    # Конфигурация Pydantic для работы с моделями SQLAlchemy.
    # from_attributes = True позволяет Pydantic читать данные
    # напрямую из атрибутов ORM-объекта (e.g., capsule.id).
    model_config = ConfigDict(from_attributes=True)
