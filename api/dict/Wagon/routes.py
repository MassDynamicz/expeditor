from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from api.dict.Wagon.schemas import WagonRelate, WagonCreate, WagonUpdate, WagonInDBBase
from api.dict.WagonType.schemas import WagonTypeInDBBase
from config.db import get_db
from api.dict.Wagon.models import Wagon
from typing import List


router = APIRouter()


# region РОУТ
@router.get("/", response_model=List[WagonRelate])
async def read_wagons(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(
            select(Wagon)
            .options(selectinload(Wagon.wagon_type))
            .offset(skip).limit(limit)
        )
        wagons = result.scalars().all()

        for wagon in wagons:
            if wagon.wagon_type:
                wagon.wagon_type_data = WagonTypeInDBBase.from_orm(wagon.wagon_type)

        return [WagonRelate.from_orm(wagon) for wagon in wagons]
    except Exception as e:
        print(f"Ошибка чтения вагона: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to read wagon: {str(e)}")


# вагона по идентификатору
@router.get("/{wagon_id}", response_model=WagonRelate)
async def read_wagon(wagon_id: int, db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(
            select(Wagon).options(selectinload(Wagon.wagon_type)).where(Wagon.id == wagon_id)
        )
        wagon = result.scalars().one_or_none()
        if wagon is None:
            raise HTTPException(status_code=404, detail="Wagon not found")

        if wagon.wagon_type:
            wagon.wagon_type_data = WagonTypeInDBBase.from_orm(wagon.wagon_type)

        return WagonRelate.from_orm(wagon)
    except Exception as e:
        print(f"Ошибка чтения вагона: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to read wagon: {str(e)}")


# Создание новой вагона или обновление существующей
@router.post("/", response_model=WagonInDBBase)
async def create_or_update_wagon(wagon: WagonCreate, db: AsyncSession = Depends(get_db)):
    try:
        # Создаем новую запись
        new_wagon = Wagon(**wagon.dict())
        db.add(new_wagon)
        await db.commit()
        await db.refresh(new_wagon)
        return WagonInDBBase.from_orm(new_wagon)
    except Exception as e:
        print(f"Ошибка создания или обновления вагона: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to create or update VAT: {str(e)}")


# Удаление вагона по идентификатору
@router.delete("/{wagon_id}", response_model=WagonInDBBase)
async def delete_wagon(wagon_id: int, db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(
            select(Wagon).where(Wagon.id == wagon_id)
        )
        wagon = result.scalars().one_or_none()
        if wagon is None:
            raise HTTPException(status_code=404, detail="Wagon not found")

        await db.delete(wagon)
        await db.commit()
        return WagonInDBBase.from_orm(wagon)
    except Exception as e:
        print(f"Ошибка удаления вагона: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to delete wagon: {str(e)}")


# Частичное обновление вагона
@router.patch("/{wagon_id}", response_model=WagonInDBBase)
async def update_wagon(wagon_id: int, wagon_update: WagonUpdate, db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(
            select(Wagon).where(Wagon.id == wagon_id)
        )
        existing_wagon = result.scalars().one_or_none()

        if existing_wagon is None:
            raise HTTPException(status_code=404, detail="Wagon not found")

        for key, value in wagon_update.dict(exclude_unset=True).items():
            setattr(existing_wagon, key, value)

        await db.commit()
        await db.refresh(existing_wagon)
        return WagonInDBBase.from_orm(existing_wagon)
    except Exception as e:
        print(f"Ошибка частичного обновления вагона: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to update wagon: {str(e)}")
# endregion
