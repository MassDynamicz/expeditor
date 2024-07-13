from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from api.dict.Gng.schemas import GngInDBBase, GngCreate, GngUpdate
from config.db import get_db
from api.dict.Gng.models import Gng
from typing import List


router = APIRouter()


# region РОУТ
@router.get("/", response_model=List[GngInDBBase])
async def read_gngs(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(
            select(Gng)
            .offset(skip).limit(limit)
        )
        gngs = result.scalars().all()
        return [GngInDBBase.from_orm(gng) for gng in gngs]
    except Exception as e:
        print(f"Ошибка чтения ставок НДС: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to read gng: {str(e)}")


# НДС по идентификатору
@router.get("/{gng_id}", response_model=GngInDBBase)
async def read_gng(gng_id: int, db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(
            select(Gng).where(Gng.id == gng_id)
        )
        gng = result.scalars().one_or_none()
        if gng is None:
            raise HTTPException(status_code=404, detail="Gng not found")
        return GngInDBBase.from_orm(gng)
    except Exception as e:
        print(f"Ошибка чтения НДС: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to read GNG: {str(e)}")


# Создание новой ставки НДС или обновление существующей
@router.post("/", response_model=GngInDBBase)
async def create_or_update_gng(gng: GngCreate, db: AsyncSession = Depends(get_db)):
    try:
        # Создаем новую запись
        new_gng = Gng(**gng.dict())
        db.add(new_gng)
        await db.commit()
        await db.refresh(new_gng)
        return GngInDBBase.from_orm(new_gng)
    except Exception as e:
        print(f"Ошибка создания или обновления НДС: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to create or update VAT: {str(e)}")


# Удаление ставки НДС по идентификатору
@router.delete("/{gng_id}", response_model=GngInDBBase)
async def delete_gng(gng_id: int, db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(
            select(Gng).where(Gng.id == gng_id)
        )
        gng = result.scalars().one_or_none()
        if gng is None:
            raise HTTPException(status_code=404, detail="Gng not found")

        await db.delete(gng)
        await db.commit()
        return GngInDBBase.from_orm(gng)
    except Exception as e:
        print(f"Ошибка удаления валюты: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to delete gng: {str(e)}")


# Частичное обновление ставки НДС
@router.patch("/{gng_id}", response_model=GngInDBBase)
async def update_gng(gng_id: int, gng_update: GngUpdate, db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(
            select(Gng).where(Gng.id == gng_id)
        )
        existing_gng = result.scalars().one_or_none()

        if existing_gng is None:
            raise HTTPException(status_code=404, detail="Gng not found")

        for key, value in gng_update.dict(exclude_unset=True).items():
            setattr(existing_gng, key, value)

        await db.commit()
        await db.refresh(existing_gng)
        return GngInDBBase.from_orm(existing_gng)
    except Exception as e:
        print(f"Ошибка частичного обновления валюты: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to update gng: {str(e)}")
# endregion
