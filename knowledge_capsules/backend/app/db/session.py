from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

# Создаем движок SQLAlchemy
engine = create_engine(settings.DATABASE_URL)

# SessionLocal будет использоваться для взаимодействия с БД
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
