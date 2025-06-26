from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base import Base

class Capsule(Base):
    """
    Модель SQLAlchemy для "капсулы знаний".
    """
    __tablename__ = "capsules"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), index=True, nullable=True)
    content = Column(Text, nullable=False)
    source_url = Column(String(2048), nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    # Дата, когда должно быть отправлено напоминание
    send_at = Column(DateTime(timezone=True), nullable=False) 
    is_sent = Column(Boolean(), default=False)

    # Внешний ключ для связи с таблицей пользователей
    owner_id = Column(Integer, ForeignKey("users.id"))
    
    # Определяет отношение "один ко многим": один пользователь может иметь много капсул.
    # 'back_populates' обеспечивает двустороннюю связь с моделью User.
    owner = relationship("User", back_populates="capsules")
