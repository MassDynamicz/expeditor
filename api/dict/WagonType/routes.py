from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from api.dict.WagonType.schemas import WagonTypeInDBBase, WagonTypeCreate, WagonTypeUpdate
from config.db import get_db
from api.dict.WagonType.models import WagonType
from typing import List


router = APIRouter()


# region РОУТ
@router.get("/", response_model=List[WagonTypeInDBBase])
async def read_wagon_types(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(
            select(WagonType)
            .offset(skip).limit(limit)
        )
        wagon_types = result.scalars().all()
        return [WagonTypeInDBBase.from_orm(wagon_type) for wagon_type in wagon_types]
    except Exception as e:
        print(f"Ошибка чтения родов ПС: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to read wagon_type: {str(e)}")


# ПС по идентификатору
@router.get("/{wagon_type_id}", response_model=WagonTypeInDBBase)
async def read_wagon_type(wagon_type_id: int, db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(
            select(WagonType).where(WagonType.id == wagon_type_id)
        )
        wagon_type = result.scalars().one_or_none()
        if wagon_type is None:
            raise HTTPException(status_code=404, detail="WagonType not found")
        return WagonTypeInDBBase.from_orm(wagon_type)
    except Exception as e:
        print(f"Ошибка чтения родов ПС: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to read VAT: {str(e)}")


# Создание новой или обновление существующей
@router.post("/", response_model=WagonTypeInDBBase)
async def create_or_update_wagon_type(wagon_type: WagonTypeCreate, db: AsyncSession = Depends(get_db)):
    try:
        # Создаем новую запись
        new_wagon_type = WagonType(**wagon_type.dict())
        db.add(new_wagon_type)
        await db.commit()
        await db.refresh(new_wagon_type)
        return WagonTypeInDBBase.from_orm(new_wagon_type)
    except Exception as e:
        print(f"Ошибка создания или обновления ПС: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to create or update VAT: {str(e)}")


# Удаление по идентификатору
@router.delete("/{wagon_type_id}", response_model=WagonTypeInDBBase)
async def delete_wagon_type(wagon_type_id: int, db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(
            select(WagonType).where(WagonType.id == wagon_type_id)
        )
        wagon_type = result.scalars().one_or_none()
        if wagon_type is None:
            raise HTTPException(status_code=404, detail="WagonType not found")

        await db.delete(wagon_type)
        await db.commit()
        return WagonTypeInDBBase.from_orm(wagon_type)
    except Exception as e:
        print(f"Ошибка удаления валюты: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to delete wagon_type: {str(e)}")


# Частичное обновление
@router.patch("/{wagon_type_id}", response_model=WagonTypeInDBBase)
async def update_wagon_type(wagon_type_id: int, wagon_type_update: WagonTypeUpdate, db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(
            select(WagonType).where(WagonType.id == wagon_type_id)
        )
        existing_wagon_type = result.scalars().one_or_none()

        if existing_wagon_type is None:
            raise HTTPException(status_code=404, detail="WagonType not found")

        for key, value in wagon_type_update.dict(exclude_unset=True).items():
            setattr(existing_wagon_type, key, value)

        await db.commit()
        await db.refresh(existing_wagon_type)
        return WagonTypeInDBBase.from_orm(existing_wagon_type)
    except Exception as e:
        print(f"Ошибка частичного обновления валюты: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to update wagon_type: {str(e)}")
# endregion
