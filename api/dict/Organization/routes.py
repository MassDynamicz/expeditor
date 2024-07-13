from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from config.db import get_db
from api.dict.Organization.models import Organization
from api.dict.Organization.schemas import OrganizationInDBBase, OrganizationCreate, OrganizationUpdate, OrganizationRelate
from typing import List
from api.dict.Country.schemas import CountryInDBBase

router = APIRouter()


# Список
@router.get("/", response_model=List[OrganizationRelate])
async def read_organizations(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(
            select(Organization)
            .options(selectinload(Organization.country))
            .offset(skip).limit(limit)
        )
        organizations = result.scalars().all()

        # Заполнение данных country_data для каждой организации
        for organization in organizations:
            if organization.country:
                organization.country_data = CountryInDBBase.from_orm(organization.country)

        return organizations

    except Exception as e:
        print(f"Ошибка чтения организаций: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to read organizations: {str(e)}")


@router.get("/{organization_id}", response_model=OrganizationRelate)
async def read_organization(organization_id: int, db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(
            select(Organization)
            .options(selectinload(Organization.country))
            .where(Organization.id == organization_id)
        )
        organization = result.scalars().one_or_none()
        if organization is None:
            raise HTTPException(status_code=404, detail="Organization not found")

        # Заполнение данных country_data для организации
        if organization.country:
            organization.country_data = CountryInDBBase.from_orm(organization.country)

        return OrganizationRelate.from_orm(organization)
    except Exception as e:
        print(f"Ошибка чтения организаций: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to read organization: {str(e)}")


@router.post("/", response_model=OrganizationInDBBase)
async def create_or_update_organization(organization: OrganizationCreate, db: AsyncSession = Depends(get_db)):
    try:
        if organization.guid == "":
            # Создаем новую запись
            new_organization = Organization(**organization.dict())
            db.add(new_organization)
            await db.commit()
            await db.refresh(new_organization)
            return OrganizationInDBBase.from_orm(new_organization)

        result = await db.execute(
            select(Organization).where(Organization.guid == organization.guid)
        )
        existing_organization = result.scalars().one_or_none()

        if existing_organization:
            # Обновляем существующую запись
            for key, value in organization.dict().items():
                setattr(existing_organization, key, value)
            await db.commit()
            await db.refresh(existing_organization)
            return OrganizationInDBBase.from_orm(existing_organization)
        else:
            # Создаем новую запись
            new_organization = Organization(**organization.dict())
            db.add(new_organization)
            await db.commit()
            await db.refresh(new_organization)
            return OrganizationInDBBase.from_orm(new_organization)
    except Exception as e:
        print(f"Ошибка создания или обновления организаций: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to create or update organization: {str(e)}")


@router.delete("/{organization_id}", response_model=OrganizationInDBBase)
async def delete_organization(organization_id: int, db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(
            select(Organization).where(Organization.id == organization_id)
        )
        organization = result.scalars().one_or_none()
        if organization is None:
            raise HTTPException(status_code=404, detail="Organization not found")

        await db.delete(organization)
        await db.commit()
        return OrganizationInDBBase.from_orm(organization)
    except Exception as e:
        print(f"Ошибка удаления организаций: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to delete organization: {str(e)}")


@router.patch("/{organization_id}", response_model=OrganizationInDBBase)
async def update_organization(
        organization_id: int,
        organization_update: OrganizationUpdate,
        db: AsyncSession = Depends(get_db)
):
    try:
        result = await db.execute(
            select(Organization).where(Organization.id == organization_id)
        )
        existing_organization = result.scalars().one_or_none()

        if existing_organization is None:
            raise HTTPException(status_code=404, detail="Organization not found")

        for key, value in organization_update.dict(exclude_unset=True).items():
            setattr(existing_organization, key, value)

        await db.commit()
        await db.refresh(existing_organization)
        return OrganizationInDBBase.from_orm(existing_organization)
    except Exception as e:
        print(f"Ошибка частичного обновления организаций: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to update organization: {str(e)}")
