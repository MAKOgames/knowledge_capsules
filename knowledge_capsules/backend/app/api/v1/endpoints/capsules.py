# app/api/v1/endpoints/capsules.py

from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import schemas, models, crud
from app.api import deps

# Создаем новый роутер для эндпоинтов, связанных с капсулами
router = APIRouter()


@router.post("/", response_model=schemas.Capsule)
def create_capsule(
    *,
    db: Session = Depends(deps.get_db),
    capsule_in: schemas.CapsuleCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Создать новую капсулу знаний.
    Капсула будет автоматически привязана к текущему пользователю.
    """
    # Вызываем CRUD-функцию для создания объекта в базе данных
    capsule = crud.capsule.create_with_owner(
        db=db, obj_in=capsule_in, owner_id=current_user.id
    )
    return capsule


@router.get("/", response_model=List[schemas.Capsule])
def read_capsules(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Получить список всех капсул, принадлежащих текущему пользователю.
    """
    # Вызываем CRUD-функцию для получения списка капсул по ID владельца
    capsules = crud.capsule.get_multi_by_owner(
        db=db, owner_id=current_user.id, skip=skip, limit=limit
    )
    return capsules


@router.get("/{capsule_id}", response_model=schemas.Capsule)
def read_capsule(
    *,
    db: Session = Depends(deps.get_db),
    capsule_id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Получить конкретную капсулу по ее ID.
    """
    # Получаем капсулу из базы данных
    capsule = crud.capsule.get(db=db, id=capsule_id)
    if not capsule:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Капсула не найдена."
        )
    # Проверяем, является ли текущий пользователь владельцем капсулы
    if capsule.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Недостаточно прав."
        )
    return capsule


@router.put("/{capsule_id}", response_model=schemas.Capsule)
def update_capsule(
    *,
    db: Session = Depends(deps.get_db),
    capsule_id: int,
    capsule_in: schemas.CapsuleUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Обновить капсулу.
    """
    capsule = crud.capsule.get(db=db, id=capsule_id)
    if not capsule:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Капсула не найдена."
        )
    if capsule.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Недостаточно прав."
        )
    # Обновляем данные капсулы в базе
    capsule = crud.capsule.update(db=db, db_obj=capsule, obj_in=capsule_in)
    return capsule


@router.delete("/{capsule_id}", response_model=schemas.Capsule)
def delete_capsule(
    *,
    db: Session = Depends(deps.get_db),
    capsule_id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Удалить капсулу.
    """
    capsule = crud.capsule.get(db=db, id=capsule_id)
    if not capsule:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Капсула не найдена."
        )
    if capsule.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Недостаточно прав."
        )
    # Удаляем капсулу из базы
    capsule = crud.capsule.remove(db=db, id=capsule_id)
    return capsule