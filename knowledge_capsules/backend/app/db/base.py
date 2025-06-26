# app/db/base.py

from sqlalchemy.orm import declarative_base

# Создаем базовый класс для всех моделей SQLAlchemy.
# Все ваши классы моделей (User, Capsule и т.д.) должны наследоваться от этого класса.
Base = declarative_base()
