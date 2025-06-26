# app/schemas/token.py

from typing import Optional

from pydantic import BaseModel


class Token(BaseModel):
    """
    Схема для JWT токена, который возвращается пользователю при логине.
    """
    access_token: str
    token_type: str


class TokenData(BaseModel):
    """
    Схема для данных, которые кодируются внутри JWT токена.
    """
    id: Optional[int] = None
