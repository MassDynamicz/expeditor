from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from api.dict.Vat.schemas import VatInDBBase, VatCreate, VatUpdate
from config.db import get_db
from api.dict.Vat.models import Vat
from typing import List


router = APIRouter()


# region РОУТ
# Список ставок НДС
@router.get("/", response_model=List[VatInDBBase])
async def read_vats(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(
            select(Vat)
            .offset(skip).limit(limit)
        )
        vats = result.scalars().all()
        return [VatInDBBase.from_orm(vat) for vat in vats]
    except Exception as e:
        print(f"Ошибка чтения ставок НДС: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to read vat: {str(e)}")


# НДС по идентификатору
@router.get("/{vat_id}", response_model=VatInDBBase)
async def read_vat(vat_id: int, db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(
            select(Vat).where(Vat.id == vat_id)
        )
        vat = result.scalars().one_or_none()
        if vat is None:
            raise HTTPException(status_code=404, detail="Vat not found")
        return VatInDBBase.from_orm(vat)
    except Exception as e:
        print(f"Ошибка чтения НДС: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to read VAT: {str(e)}")


# Создание новой ставки НДС или обновление существующей
@router.post("/", response_model=VatInDBBase)
async def create_or_update_vat(vat: VatCreate, db: AsyncSession = Depends(get_db)):
    try:
        if vat.guid == "":
            # Создаем новую запись
            new_vat = Vat(**vat.dict())
            db.add(new_vat)
            await db.commit()
            await db.refresh(new_vat)
            return VatInDBBase.from_orm(new_vat)

        result = await db.execute(
            select(Vat).where(Vat.guid == vat.guid)
        )
        existing_vat = result.scalars().one_or_none()

        if existing_vat:
            # Обновляем существующую запись
            for key, value in vat.dict().items():
                setattr(existing_vat, key, value)
            await db.commit()
            await db.refresh(existing_vat)
            return VatInDBBase.from_orm(existing_vat)
        else:
            # Создаем новую запись
            new_vat = Vat(**vat.dict())
            db.add(new_vat)
            await db.commit()
            await db.refresh(new_vat)
            return VatInDBBase.from_orm(new_vat)
    except Exception as e:
        print(f"Ошибка создания или обновления НДС: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to create or update VAT: {str(e)}")


# Удаление ставки НДС по идентификатору
@router.delete("/{vat_id}", response_model=VatInDBBase)
async def delete_vat(vat_id: int, db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(
            select(Vat).where(Vat.id == vat_id)
        )
        vat = result.scalars().one_or_none()
        if vat is None:
            raise HTTPException(status_code=404, detail="Vat not found")

        await db.delete(vat)
        await db.commit()
        return VatInDBBase.from_orm(vat)
    except Exception as e:
        print(f"Ошибка удаления валюты: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to delete vat: {str(e)}")


# Частичное обновление ставки НДС
@router.patch("/{vat_id}", response_model=VatInDBBase)
async def update_vat(vat_id: int, vat_update: VatUpdate, db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(
            select(Vat).where(Vat.id == vat_id)
        )
        existing_vat = result.scalars().one_or_none()

        if existing_vat is None:
            raise HTTPException(status_code=404, detail="Vat not found")

        for key, value in vat_update.dict(exclude_unset=True).items():
            setattr(existing_vat, key, value)

        await db.commit()
        await db.refresh(existing_vat)
        return VatInDBBase.from_orm(existing_vat)
    except Exception as e:
        print(f"Ошибка частичного обновления валюты: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to update vat: {str(e)}")
# endregion
