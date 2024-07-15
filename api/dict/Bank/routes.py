from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from api.dict.Bank.schemas import BankInDBBase, BankCreate, BankUpdate
from config.db import get_db
from api.dict.Bank.models import Bank
from typing import List


router = APIRouter()


# region РОУТ
@router.get("/", response_model=List[BankInDBBase])
async def read_banks(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(
            select(Bank)
            .offset(skip).limit(limit)
        )
        banks = result.scalars().all()
        return [BankInDBBase.from_orm(bank) for bank in banks]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to read bank: {str(e)}")


@router.get("/{bank_id}", response_model=BankInDBBase)
async def read_bank(bank_id: int, db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(
            select(Bank).where(Bank.id == bank_id)
        )
        bank = result.scalars().one_or_none()
        if bank is None:
            raise HTTPException(status_code=404, detail="Bank not found")
        return BankInDBBase.from_orm(bank)
    except Exception as e:
        print(f"Ошибка чтения банков: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to read VAT: {str(e)}")


@router.post("/", response_model=BankInDBBase)
async def create_or_update_bank(bank: BankCreate, db: AsyncSession = Depends(get_db)):
    try:
        if bank.guid == "":
            # Создаем новую запись
            new_bank = Bank(**bank.dict())
            db.add(new_bank)
            await db.commit()
            await db.refresh(new_bank)
            return BankInDBBase.from_orm(new_bank)

        result = await db.execute(
            select(Bank).where(Bank.guid == bank.guid)
        )
        existing_bank = result.scalars().one_or_none()

        if existing_bank:
            # Обновляем существующую запись
            for key, value in bank.dict().items():
                setattr(existing_bank, key, value)
            await db.commit()
            await db.refresh(existing_bank)
            return BankInDBBase.from_orm(existing_bank)
        else:
            # Создаем новую запись
            new_bank = Bank(**bank.dict())
            db.add(new_bank)
            await db.commit()
            await db.refresh(new_bank)
            return BankInDBBase.from_orm(new_bank)
    except Exception as e:
        print(f"Ошибка создания или обновления банков: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to create or update Bank: {str(e)}")


@router.delete("/{bank_id}", response_model=BankInDBBase)
async def delete_bank(bank_id: int, db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(
            select(Bank).where(Bank.id == bank_id)
        )
        bank = result.scalars().one_or_none()
        if bank is None:
            raise HTTPException(status_code=404, detail="Bank not found")

        await db.delete(bank)
        await db.commit()
        return BankInDBBase.from_orm(bank)
    except Exception as e:
        print(f"Ошибка удаления валюты: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to delete bank: {str(e)}")


@router.patch("/{bank_id}", response_model=BankInDBBase)
async def update_bank(bank_id: int, bank_update: BankUpdate, db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(
            select(Bank).where(Bank.id == bank_id)
        )
        existing_bank = result.scalars().one_or_none()

        if existing_bank is None:
            raise HTTPException(status_code=404, detail="Bank not found")

        for key, value in bank_update.dict(exclude_unset=True).items():
            setattr(existing_bank, key, value)

        await db.commit()
        await db.refresh(existing_bank)
        return BankInDBBase.from_orm(existing_bank)
    except Exception as e:
        print(f"Ошибка частичного обновления банков: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to update bank: {str(e)}")
# endregion
