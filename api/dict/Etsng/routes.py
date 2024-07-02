from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from api.dict.Etsng.schemas import EtsngInDBBase, EtsngCreate, EtsngUpdate
from config.db import get_db
from api.dict.Etsng.models import Etsng
from typing import List


router = APIRouter()


# region РОУТ
@router.get("/", response_model=List[EtsngInDBBase])
async def read_etsngs(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(
            select(Etsng)
            .offset(skip).limit(limit)
        )
        etsngs = result.scalars().all()
        return [EtsngInDBBase.from_orm(etsng) for etsng in etsngs]
    except Exception as e:
        print(f"Ошибка чтения ставок НДС: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to read etsng: {str(e)}")


# НДС по идентификатору
@router.get("/{etsng_id}", response_model=EtsngInDBBase)
async def read_etsng(etsng_id: int, db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(
            select(Etsng).where(Etsng.id == etsng_id)
        )
        etsng = result.scalars().one_or_none()
        if etsng is None:
            raise HTTPException(status_code=404, detail="Etsng not found")
        return EtsngInDBBase.from_orm(etsng)
    except Exception as e:
        print(f"Ошибка чтения НДС: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to read VAT: {str(e)}")


# Создание новой ставки НДС или обновление существующей
@router.post("/", response_model=EtsngInDBBase)
async def create_or_update_etsng(etsng: EtsngCreate, db: AsyncSession = Depends(get_db)):
    try:
        # Создаем новую запись
        new_etsng = Etsng(**etsng.dict())
        db.add(new_etsng)
        await db.commit()
        await db.refresh(new_etsng)
        return EtsngInDBBase.from_orm(new_etsng)
    except Exception as e:
        print(f"Ошибка создания или обновления НДС: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to create or update ETSNG: {str(e)}")


# Удаление ставки НДС по идентификатору
@router.delete("/{etsng_id}", response_model=EtsngInDBBase)
async def delete_etsng(etsng_id: int, db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(
            select(Etsng).where(Etsng.id == etsng_id)
        )
        etsng = result.scalars().one_or_none()
        if etsng is None:
            raise HTTPException(status_code=404, detail="Etsng not found")

        await db.delete(etsng)
        await db.commit()
        return EtsngInDBBase.from_orm(etsng)
    except Exception as e:
        print(f"Ошибка удаления валюты: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to delete etsng: {str(e)}")


# Частичное обновление ставки НДС
@router.patch("/{etsng_id}", response_model=EtsngInDBBase)
async def update_etsng(etsng_id: int, etsng_update: EtsngUpdate, db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(
            select(Etsng).where(Etsng.id == etsng_id)
        )
        existing_etsng = result.scalars().one_or_none()

        if existing_etsng is None:
            raise HTTPException(status_code=404, detail="Etsng not found")

        for key, value in etsng_update.dict(exclude_unset=True).items():
            setattr(existing_etsng, key, value)

        await db.commit()
        await db.refresh(existing_etsng)
        return EtsngInDBBase.from_orm(existing_etsng)
    except Exception as e:
        print(f"Ошибка частичного обновления валюты: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to update etsng: {str(e)}")
# endregion
