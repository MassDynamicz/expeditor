from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from config.db import get_db
from api.dict.Contract.models import Contract
from api.dict.Contract.schemas import ContractInDBBase, ContractRelate, ContractCreate, ContractUpdate
from typing import List
from api.dict.Organization.schemas import OrganizationRelate
from api.dict.Currency.schemas import CurrencyInDBBase
from api.dict.Contractor.schemas import ContractorRelate

router = APIRouter()


# Список
@router.get("/", response_model=List[ContractRelate])
async def read_contracts(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(
            select(Contract)
            .options(
                selectinload(Contract.organization),
                selectinload(Contract.contractor),
                selectinload(Contract.currency)
            )
            .offset(skip).limit(limit)
        )
        contracts = result.scalars().all()

        # Заполнение данных country_data для каждой организации
        for contract in contracts:
            if contract.organization:
                contract.organization_data = OrganizationRelate.from_orm(contract.organization)
            if contract.contractor:
                contract.contractor_data = ContractorRelate.from_orm(contract.contractor)
            if contract.organization:
                contract.currency_data = CurrencyInDBBase.from_orm(contract.currency)

        return contracts

    except Exception as e:
        print(f"Ошибка чтения договоров: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to read contracts: {str(e)}")


@router.get("/{contract_id}", response_model=ContractRelate)
async def read_contract(contract_id: int, db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(
            select(Contract)
            .options(
                selectinload(Contract.organization),
                selectinload(Contract.contractor),
                selectinload(Contract.currency)
            )
            .where(Contract.id == contract_id)
        )
        contract = result.scalars().one_or_none()
        if contract is None:
            raise HTTPException(status_code=404, detail="Contract not found")

        if contract.organization:
            contract.organization_data = OrganizationRelate.from_orm(contract.organization)
        if contract.contractor:
            contract.contractor_data = ContractorRelate.from_orm(contract.contractor)
        if contract.organization:
            contract.currency_data = CurrencyInDBBase.from_orm(contract.currency)

        return ContractRelate.from_orm(contract)
    except Exception as e:
        print(f"Ошибка чтения договоров: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to read contract: {str(e)}")


@router.post("/", response_model=ContractInDBBase)
async def create_or_update_contract(contract: ContractCreate, db: AsyncSession = Depends(get_db)):
    try:
        if contract.guid == "":
            # Создаем новую запись
            new_contract = Contract(**contract.dict())
            db.add(new_contract)
            await db.commit()
            await db.refresh(new_contract)
            return ContractInDBBase.from_orm(new_contract)

        result = await db.execute(
            select(Contract).where(Contract.guid == contract.guid)
        )
        existing_contract = result.scalars().one_or_none()

        if existing_contract:
            # Обновляем существующую запись
            for key, value in contract.dict().items():
                setattr(existing_contract, key, value)
            await db.commit()
            await db.refresh(existing_contract)
            return ContractInDBBase.from_orm(existing_contract)
        else:
            # Создаем новую запись
            new_contract = Contract(**contract.dict())
            db.add(new_contract)
            await db.commit()
            await db.refresh(new_contract)
            return ContractInDBBase.from_orm(new_contract)
    except Exception as e:
        print(f"Ошибка создания или обновления договоров: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to create or update contract: {str(e)}")


@router.delete("/{contract_id}", response_model=ContractInDBBase)
async def delete_contract(contract_id: int, db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(
            select(Contract).where(Contract.id == contract_id)
        )
        contract = result.scalars().one_or_none()
        if contract is None:
            raise HTTPException(status_code=404, detail="Contract not found")

        await db.delete(contract)
        await db.commit()
        return ContractInDBBase.from_orm(contract)
    except Exception as e:
        print(f"Ошибка удаления договоров: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to delete contract: {str(e)}")


@router.patch("/{contract_id}", response_model=ContractInDBBase)
async def update_contract(contract_id: int, contract_update: ContractUpdate, db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(
            select(Contract).where(Contract.id == contract_id)
        )
        existing_contract = result.scalars().one_or_none()

        if existing_contract is None:
            raise HTTPException(status_code=404, detail="Contract not found")

        for key, value in contract_update.dict(exclude_unset=True).items():
            setattr(existing_contract, key, value)

        await db.commit()
        await db.refresh(existing_contract)
        return ContractInDBBase.from_orm(existing_contract)
    except Exception as e:
        print(f"Ошибка частичного обновления договоров: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to update contract: {str(e)}")
