from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from config.db import get_db
from api.dict.BankAccountOrg.models import BankAccountOrg
from api.dict.BankAccountOrg.schemas import BankAccountOrgInDBBase, BankAccountOrgRelate, BankAccountOrgCreate, BankAccountOrgUpdate
from typing import List
from api.dict.Bank.schemas import BankInDBBase
from api.dict.Currency.schemas import CurrencyInDBBase
from api.dict.Organization.schemas import OrganizationInDBBase

router = APIRouter()


# Список
@router.get("/", response_model=List[BankAccountOrgRelate])
async def read_bank_account_orgs(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(
            select(BankAccountOrg)
            .options(
                selectinload(BankAccountOrg.currency),
                selectinload(BankAccountOrg.bank),
                selectinload(BankAccountOrg.owner)
            )
            .offset(skip).limit(limit)
        )
        bank_account_orgs = result.scalars().all()

        # Заполнение данных country_data для каждой организации
        for bank_account_org in bank_account_orgs:
            if bank_account_org.currency:
                bank_account_org.currency_data = CurrencyInDBBase.from_orm(bank_account_org.currency)
            if bank_account_org.bank:
                bank_account_org.bank_data = BankInDBBase.from_orm(bank_account_org.bank)
            if bank_account_org.owner:
                bank_account_org.owner_data = OrganizationInDBBase.from_orm(bank_account_org.owner)

        return bank_account_orgs

    except Exception as e:
        print(f"Ошибка чтения банк счетов: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to read bank_account_orgs: {str(e)}")


@router.get("/{bank_account_org_id}", response_model=BankAccountOrgRelate)
async def read_bank_account_org(bank_account_org_id: int, db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(
            select(BankAccountOrg)
            .options(
                selectinload(BankAccountOrg.currency),
                selectinload(BankAccountOrg.owner),
                selectinload(BankAccountOrg.bank)
            )
            .where(BankAccountOrg.id == bank_account_org_id)
        )
        bank_account_org = result.scalars().one_or_none()
        if bank_account_org is None:
            raise HTTPException(status_code=404, detail="BankAccountOrg not found")

        if bank_account_org.owner:
            bank_account_org.owner_data = OrganizationInDBBase.from_orm(bank_account_org.owner)
        if bank_account_org.currency:
            bank_account_org.currency_data = CurrencyInDBBase.from_orm(bank_account_org.currency)
        if bank_account_org.bank:
            bank_account_org.bank_data = BankInDBBase.from_orm(bank_account_org.bank)

        return BankAccountOrgRelate.from_orm(bank_account_org)
    except Exception as e:
        print(f"Ошибка чтения банк счетов: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to read bank_account_org: {str(e)}")


@router.post("/", response_model=BankAccountOrgInDBBase)
async def create_or_update_bank_account_org(bank_account_org: BankAccountOrgCreate, db: AsyncSession = Depends(get_db)):
    try:
        if bank_account_org.guid == "":
            # Создаем новую запись
            new_bank_account_org = BankAccountOrg(**bank_account_org.dict())
            db.add(new_bank_account_org)
            await db.commit()
            await db.refresh(new_bank_account_org)
            return BankAccountOrgInDBBase.from_orm(new_bank_account_org)

        result = await db.execute(
            select(BankAccountOrg).where(BankAccountOrg.guid == bank_account_org.guid)
        )
        existing_bank_account_org = result.scalars().one_or_none()

        if existing_bank_account_org:
            # Обновляем существующую запись
            for key, value in bank_account_org.dict().items():
                setattr(existing_bank_account_org, key, value)
            await db.commit()
            await db.refresh(existing_bank_account_org)
            return BankAccountOrgInDBBase.from_orm(existing_bank_account_org)
        else:
            # Создаем новую запись
            new_bank_account_org = BankAccountOrg(**bank_account_org.dict())
            db.add(new_bank_account_org)
            await db.commit()
            await db.refresh(new_bank_account_org)
            return BankAccountOrgInDBBase.from_orm(new_bank_account_org)
    except Exception as e:
        print(f"Ошибка создания или обновления банк счетов: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to create or update bank_account_org: {str(e)}")


@router.delete("/{bank_account_org_id}", response_model=BankAccountOrgInDBBase)
async def delete_bank_account_org(bank_account_org_id: int, db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(
            select(BankAccountOrg).where(BankAccountOrg.id == bank_account_org_id)
        )
        bank_account_org = result.scalars().one_or_none()
        if bank_account_org is None:
            raise HTTPException(status_code=404, detail="BankAccountOrg not found")

        await db.delete(bank_account_org)
        await db.commit()
        return BankAccountOrgInDBBase.from_orm(bank_account_org)
    except Exception as e:
        print(f"Ошибка удаления банк счетов: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to delete bank_account_org: {str(e)}")


@router.patch("/{bank_account_org_id}", response_model=BankAccountOrgInDBBase)
async def update_bank_account_org(bank_account_org_id: int, bank_account_org_update: BankAccountOrgUpdate, db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(
            select(BankAccountOrg).where(BankAccountOrg.id == bank_account_org_id)
        )
        existing_bank_account_org = result.scalars().one_or_none()

        if existing_bank_account_org is None:
            raise HTTPException(status_code=404, detail="BankAccountOrg not found")

        for key, value in bank_account_org_update.dict(exclude_unset=True).items():
            setattr(existing_bank_account_org, key, value)

        await db.commit()
        await db.refresh(existing_bank_account_org)
        return BankAccountOrgInDBBase.from_orm(existing_bank_account_org)
    except Exception as e:
        print(f"Ошибка частичного обновления банк счетов: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to update bank_account_org: {str(e)}")
