from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from config.db import get_db
from api.dict.BankAccount.models import BankAccount
from api.dict.BankAccount.schemas import BankAccountInDBBase, BankAccountRelate, BankAccountCreate, BankAccountUpdate
from typing import List
from api.dict.Bank.schemas import BankInDBBase
from api.dict.Currency.schemas import CurrencyInDBBase
from api.dict.Contractor.schemas import ContractorInDBBase

router = APIRouter()


# Список
@router.get("/", response_model=List[BankAccountRelate])
async def read_bank_accounts(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(
            select(BankAccount)
            .options(
                selectinload(BankAccount.currency),
                selectinload(BankAccount.bank),
                selectinload(BankAccount.owner)
            )
            .offset(skip).limit(limit)
        )
        bank_accounts = result.scalars().all()

        # Заполнение данных country_data для каждой организации
        for bank_account in bank_accounts:
            if bank_account.currency:
                bank_account.currency_data = CurrencyInDBBase.from_orm(bank_account.currency)
            if bank_account.bank:
                bank_account.bank_data = BankInDBBase.from_orm(bank_account.bank)
            if bank_account.owner:
                bank_account.owner_data = ContractorInDBBase.from_orm(bank_account.owner)

        return bank_accounts

    except Exception as e:
        print(f"Ошибка чтения банк счетов: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to read bank_accounts: {str(e)}")


@router.get("/{bank_account_id}", response_model=BankAccountRelate)
async def read_bank_account(bank_account_id: int, db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(
            select(BankAccount)
            .options(
                selectinload(BankAccount.currency),
                selectinload(BankAccount.owner),
                selectinload(BankAccount.bank)
            )
            .where(BankAccount.id == bank_account_id)
        )
        bank_account = result.scalars().one_or_none()
        if bank_account is None:
            raise HTTPException(status_code=404, detail="BankAccount not found")

        if bank_account.owner:
            bank_account.owner_data = ContractorInDBBase.from_orm(bank_account.owner)
        if bank_account.currency:
            bank_account.currency_data = CurrencyInDBBase.from_orm(bank_account.currency)
        if bank_account.bank:
            bank_account.bank_data = BankInDBBase.from_orm(bank_account.bank)

        return BankAccountRelate.from_orm(bank_account)
    except Exception as e:
        print(f"Ошибка чтения банк счетов: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to read bank_account: {str(e)}")


@router.post("/", response_model=BankAccountInDBBase)
async def create_or_update_bank_account(bank_account: BankAccountCreate, db: AsyncSession = Depends(get_db)):
    try:
        if bank_account.guid == "":
            # Создаем новую запись
            new_bank_account = BankAccount(**bank_account.dict())
            db.add(new_bank_account)
            await db.commit()
            await db.refresh(new_bank_account)
            return BankAccountInDBBase.from_orm(new_bank_account)

        result = await db.execute(
            select(BankAccount).where(BankAccount.guid == bank_account.guid)
        )
        existing_bank_account = result.scalars().one_or_none()

        if existing_bank_account:
            # Обновляем существующую запись
            for key, value in bank_account.dict().items():
                setattr(existing_bank_account, key, value)
            await db.commit()
            await db.refresh(existing_bank_account)
            return BankAccountInDBBase.from_orm(existing_bank_account)
        else:
            # Создаем новую запись
            new_bank_account = BankAccount(**bank_account.dict())
            db.add(new_bank_account)
            await db.commit()
            await db.refresh(new_bank_account)
            return BankAccountInDBBase.from_orm(new_bank_account)
    except Exception as e:
        print(f"Ошибка создания или обновления банк счетов: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to create or update bank_account: {str(e)}")


@router.delete("/{bank_account_id}", response_model=BankAccountInDBBase)
async def delete_bank_account(bank_account_id: int, db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(
            select(BankAccount).where(BankAccount.id == bank_account_id)
        )
        bank_account = result.scalars().one_or_none()
        if bank_account is None:
            raise HTTPException(status_code=404, detail="BankAccount not found")

        await db.delete(bank_account)
        await db.commit()
        return BankAccountInDBBase.from_orm(bank_account)
    except Exception as e:
        print(f"Ошибка удаления банк счетов: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to delete bank_account: {str(e)}")


@router.patch("/{bank_account_id}", response_model=BankAccountInDBBase)
async def update_bank_account(bank_account_id: int, bank_account_update: BankAccountUpdate, db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(
            select(BankAccount).where(BankAccount.id == bank_account_id)
        )
        existing_bank_account = result.scalars().one_or_none()

        if existing_bank_account is None:
            raise HTTPException(status_code=404, detail="BankAccount not found")

        for key, value in bank_account_update.dict(exclude_unset=True).items():
            setattr(existing_bank_account, key, value)

        await db.commit()
        await db.refresh(existing_bank_account)
        return BankAccountInDBBase.from_orm(existing_bank_account)
    except Exception as e:
        print(f"Ошибка частичного обновления банк счетов: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to update bank_account: {str(e)}")
