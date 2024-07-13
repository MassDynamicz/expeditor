from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from api.dict.Territory.schemas import TerritoryInDBBase, TerritoryCreate, TerritoryUpdate
from config.db import get_db
from api.dict.Territory.models import Territory
from typing import List


router = APIRouter()


# region РОУТ
@router.get("/", response_model=List[TerritoryInDBBase])
async def read_territorys(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(
            select(Territory)
            .offset(skip).limit(limit)
        )
        territorys = result.scalars().all()
        return [TerritoryInDBBase.from_orm(territory) for territory in territorys]
    except Exception as e:
        print(f"Ошибка чтения Ж/Д территорорий: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to read territory: {str(e)}")


# территорий по идентификатору
@router.get("/{territory_id}", response_model=TerritoryInDBBase)
async def read_territory(territory_id: int, db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(
            select(Territory).where(Territory.id == territory_id)
        )
        territory = result.scalars().one_or_none()
        if territory is None:
            raise HTTPException(status_code=404, detail="Territory not found")
        return TerritoryInDBBase.from_orm(territory)
    except Exception as e:
        print(f"Ошибка чтения территорий: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to read VAT: {str(e)}")


# Создание новой ставки территорий или обновление существующей
@router.post("/", response_model=TerritoryInDBBase)
async def create_or_update_territory(territory: TerritoryCreate, db: AsyncSession = Depends(get_db)):
    try:
        # Создаем новую запись
        new_territory = Territory(**territory.dict())
        db.add(new_territory)
        await db.commit()
        await db.refresh(new_territory)
        return TerritoryInDBBase.from_orm(new_territory)
    except Exception as e:
        print(f"Ошибка создания или обновления территорий: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to create or update VAT: {str(e)}")


# Удаление ставки территорий по идентификатору
@router.delete("/{territory_id}", response_model=TerritoryInDBBase)
async def delete_territory(territory_id: int, db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(
            select(Territory).where(Territory.id == territory_id)
        )
        territory = result.scalars().one_or_none()
        if territory is None:
            raise HTTPException(status_code=404, detail="Territory not found")

        await db.delete(territory)
        await db.commit()
        return TerritoryInDBBase.from_orm(territory)
    except Exception as e:
        print(f"Ошибка удаления валюты: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to delete territory: {str(e)}")


# Частичное обновление ставки территорий
@router.patch("/{territory_id}", response_model=TerritoryInDBBase)
async def update_territory(territory_id: int, territory_update: TerritoryUpdate, db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(
            select(Territory).where(Territory.id == territory_id)
        )
        existing_territory = result.scalars().one_or_none()

        if existing_territory is None:
            raise HTTPException(status_code=404, detail="Territory not found")

        for key, value in territory_update.dict(exclude_unset=True).items():
            setattr(existing_territory, key, value)

        await db.commit()
        await db.refresh(existing_territory)
        return TerritoryInDBBase.from_orm(existing_territory)
    except Exception as e:
        print(f"Ошибка частичного обновления валюты: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to update territory: {str(e)}")
# endregion
