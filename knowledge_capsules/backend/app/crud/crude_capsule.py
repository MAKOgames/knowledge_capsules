# app/crud/crud_capsule.py

from datetime import datetime
from typing import List

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.capsule import Capsule
from app.schemas.capsule import CapsuleCreate, CapsuleUpdate


class CRUDCapsule(CRUDBase[Capsule, CapsuleCreate, CapsuleUpdate]):
    def create_with_owner(
        self, db: Session, *, obj_in: CapsuleCreate, owner_id: int
    ) -> Capsule:
        """
        Создать новую капсулу с указанием владельца.
        """
        # Преобразуем Pydantic схему в словарь
        obj_in_data = obj_in.model_dump()
        # Создаем экземпляр модели SQLAlchemy, добавляя owner_id
        db_obj = self.model(**obj_in_data, owner_id=owner_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_multi_by_owner(
        self, db: Session, *, owner_id: int, skip: int = 0, limit: int = 100
    ) -> List[Capsule]:
        """
        Получить список капсул для конкретного владельца.
        """
        return (
            db.query(self.model)
            .filter(Capsule.owner_id == owner_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_due_capsules(self, db: Session) -> List[Capsule]:
        """
        Получить все капсулы, у которых подошло время отправки
        и которые еще не были отправлены.
        """
        return (
            db.query(self.model)
            .filter(Capsule.send_at <= datetime.utcnow(), Capsule.is_sent == False)
            .all()
        )


# Создаем единственный экземпляр класса для использования в приложении
capsule = CRUDCapsule(Capsule)
