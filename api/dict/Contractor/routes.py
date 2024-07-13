from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from config.db import get_db
from api.dict.Contractor.models import Contractor
from api.dict.Contractor.schemas import ContractorInDBBase, ContractorCreate, ContractorUpdate, ContractorRelate
from typing import List
from api.dict.Country.schemas import CountryInDBBase

router = APIRouter()


# Список
@router.get("/", response_model=List[ContractorRelate])
async def read_contractors(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(
            select(Contractor)
            .options(selectinload(Contractor.country))
            .offset(skip).limit(limit)
        )
        contractors = result.scalars().all()

        # Заполнение данных country_data для каждой организации
        for contractor in contractors:
            if contractor.country:
                contractor.country_data = CountryInDBBase.from_orm(contractor.country)

        return contractors

    except Exception as e:
        print(f"Ошибка чтения контрагентов: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to read contractors: {str(e)}")


@router.get("/{contractor_id}", response_model=ContractorRelate)
async def read_contractor(contractor_id: int, db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(
            select(Contractor).options(selectinload(Contractor.country)).where(Contractor.id == contractor_id)
        )
        contractor = result.scalars().one_or_none()
        if contractor is None:
            raise HTTPException(status_code=404, detail="Contractor not found")
        if contractor.country:
            contractor.country_data = CountryInDBBase.from_orm(contractor.country)

        return ContractorRelate.from_orm(contractor)
    except Exception as e:
        print(f"Ошибка чтения контрагентов: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to read contractor: {str(e)}")


@router.post("/", response_model=ContractorInDBBase)
async def create_or_update_contractor(contractor: ContractorCreate, db: AsyncSession = Depends(get_db)):
    try:
        if contractor.guid == "":
            # Создаем новую запись
            new_contractor = Contractor(**contractor.dict())
            db.add(new_contractor)
            await db.commit()
            await db.refresh(new_contractor)
            return ContractorInDBBase.from_orm(new_contractor)

        result = await db.execute(
            select(Contractor).where(Contractor.guid == contractor.guid)
        )
        existing_contractor = result.scalars().one_or_none()

        if existing_contractor:
            # Обновляем существующую запись
            for key, value in contractor.dict().items():
                setattr(existing_contractor, key, value)
            await db.commit()
            await db.refresh(existing_contractor)
            return ContractorInDBBase.from_orm(existing_contractor)
        else:
            # Создаем новую запись
            new_contractor = Contractor(**contractor.dict())
            db.add(new_contractor)
            await db.commit()
            await db.refresh(new_contractor)
            return ContractorInDBBase.from_orm(new_contractor)
    except Exception as e:
        print(f"Ошибка создания или обновления контрагентов: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to create or update contractor: {str(e)}")


@router.delete("/{contractor_id}", response_model=ContractorInDBBase)
async def delete_contractor(contractor_id: int, db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(
            select(Contractor).where(Contractor.id == contractor_id)
        )
        contractor = result.scalars().one_or_none()
        if contractor is None:
            raise HTTPException(status_code=404, detail="Contractor not found")

        await db.delete(contractor)
        await db.commit()
        return ContractorInDBBase.from_orm(contractor)
    except Exception as e:
        print(f"Ошибка удаления контрагентов: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to delete contractor: {str(e)}")


@router.patch("/{contractor_id}", response_model=ContractorInDBBase)
async def update_contractor(
        contractor_id: int,
        contractor_update: ContractorUpdate,
        db: AsyncSession = Depends(get_db)
):
    try:
        result = await db.execute(
            select(Contractor).where(Contractor.id == contractor_id)
        )
        existing_contractor = result.scalars().one_or_none()

        if existing_contractor is None:
            raise HTTPException(status_code=404, detail="Contractor not found")

        for key, value in contractor_update.dict(exclude_unset=True).items():
            setattr(existing_contractor, key, value)

        await db.commit()
        await db.refresh(existing_contractor)
        return ContractorInDBBase.from_orm(existing_contractor)
    except Exception as e:
        print(f"Ошибка частичного обновления контрагентов: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to update contractor: {str(e)}")
