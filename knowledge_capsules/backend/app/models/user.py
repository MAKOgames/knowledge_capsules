# app/models/user.py

from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship

from app.db.base import Base

class User(Base):
    """
    Модель SQLAlchemy для Пользователя.
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean(), default=True)

    # Определяет отношение "один ко многим" с моделью Capsule.
    # 'back_populates' обеспечивает двустороннюю связь.
    # 'cascade="all, delete-orphan"' означает, что при удалении пользователя
    # будут также удалены все связанные с ним капсулы.
    capsules = relationship("Capsule", back_populates="owner", cascade="all, delete-orphan")
