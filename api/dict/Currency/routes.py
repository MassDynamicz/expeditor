from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from config.db import get_db
from api.dict.Currency.models import Currency
from api.dict.Currency.schemas import CurrencyInDBBase, CurrencyCreate, CurrencyUpdate
from typing import List

router = APIRouter()


# Список валют
@router.get("/", response_model=List[CurrencyInDBBase])
async def read_currencies(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(
            select(Currency)
            .offset(skip).limit(limit)
        )
        currencies = result.scalars().all()
        return [CurrencyInDBBase.from_orm(currency) for currency in currencies]
    except Exception as e:
        print(f"Ошибка чтения валют: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to read currencies: {str(e)}")


# Валюта по идентификатору
@router.get("/{currency_id}", response_model=CurrencyInDBBase)
async def read_currency(currency_id: int, db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(
            select(Currency).where(Currency.id == currency_id)
        )
        currency = result.scalars().one_or_none()
        if currency is None:
            raise HTTPException(status_code=404, detail="Currency not found")
        return CurrencyInDBBase.from_orm(currency)
    except Exception as e:
        print(f"Ошибка чтения валюты: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to read currency: {str(e)}")


# Создание новой валюты или обновление существующей
@router.post("/", response_model=CurrencyInDBBase)
async def create_or_update_currency(currency: CurrencyCreate, db: AsyncSession = Depends(get_db)):
    try:
        if currency.guid == "":
            # Создаем новую запись
            new_currency = Currency(**currency.dict())
            db.add(new_currency)
            await db.commit()
            await db.refresh(new_currency)
            return CurrencyInDBBase.from_orm(new_currency)

        result = await db.execute(
            select(Currency).where(Currency.guid == currency.guid)
        )
        existing_currency = result.scalars().one_or_none()

        if existing_currency:
            # Обновляем существующую запись
            for key, value in currency.dict().items():
                setattr(existing_currency, key, value)
            await db.commit()
            await db.refresh(existing_currency)
            return CurrencyInDBBase.from_orm(existing_currency)
        else:
            # Создаем новую запись
            new_currency = Currency(**currency.dict())
            db.add(new_currency)
            await db.commit()
            await db.refresh(new_currency)
            return CurrencyInDBBase.from_orm(new_currency)
    except Exception as e:
        print(f"Ошибка создания или обновления валюты: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to create or update currency: {str(e)}")


# Удаление валюты по идентификатору
@router.delete("/{currency_id}", response_model=CurrencyInDBBase)
async def delete_currency(currency_id: int, db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(
            select(Currency).where(Currency.id == currency_id)
        )
        currency = result.scalars().one_or_none()
        if currency is None:
            raise HTTPException(status_code=404, detail="Currency not found")

        await db.delete(currency)
        await db.commit()
        return CurrencyInDBBase.from_orm(currency)
    except Exception as e:
        print(f"Ошибка удаления валюты: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to delete currency: {str(e)}")


# Частичное обновление валюты
@router.patch("/{currency_id}", response_model=CurrencyInDBBase)
async def update_currency(currency_id: int, currency_update: CurrencyUpdate, db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(
            select(Currency).where(Currency.id == currency_id)
        )
        existing_currency = result.scalars().one_or_none()

        if existing_currency is None:
            raise HTTPException(status_code=404, detail="Currency not found")

        for key, value in currency_update.dict(exclude_unset=True).items():
            setattr(existing_currency, key, value)

        await db.commit()
        await db.refresh(existing_currency)
        return CurrencyInDBBase.from_orm(existing_currency)
    except Exception as e:
        print(f"Ошибка частичного обновления валюты: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to update currency: {str(e)}")
