from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from api.dict.ServiceType.schemas import ServiceTypeInDBBase, ServiceTypeCreate, ServiceTypeUpdate
from config.db import get_db
from api.dict.ServiceType.models import ServiceType
from typing import List


router = APIRouter()


@router.get("/", response_model=List[ServiceTypeInDBBase])
async def read_service_types(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(
            select(ServiceType)
            .offset(skip).limit(limit)
        )
        service_types = result.scalars().all()
        return [ServiceTypeInDBBase.from_orm(service_type) for service_type in service_types]
    except Exception as e:
        print(f"Ошибка чтения видов услуг: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to read service_type: {str(e)}")


@router.get("/{service_type_id}", response_model=ServiceTypeInDBBase)
async def read_service_type(service_type_id: int, db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(
            select(ServiceType).where(ServiceType.id == service_type_id)
        )
        service_type = result.scalars().one_or_none()
        if service_type is None:
            raise HTTPException(status_code=404, detail="ServiceType not found")
        return ServiceTypeInDBBase.from_orm(service_type)
    except Exception as e:
        print(f"Ошибка чтения видов услуг: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to read service type: {str(e)}")


@router.post("/", response_model=ServiceTypeInDBBase)
async def create_or_update_service_type(service_type: ServiceTypeCreate, db: AsyncSession = Depends(get_db)):
    try:
        # Создаем новую запись
        new_service_type = ServiceType(**service_type.dict())
        db.add(new_service_type)
        await db.commit()
        await db.refresh(new_service_type)
        return ServiceTypeInDBBase.from_orm(new_service_type)
    except Exception as e:
        print(f"Ошибка создания или обновления видов услуг: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to create or update VAT: {str(e)}")


@router.delete("/{service_type_id}", response_model=ServiceTypeInDBBase)
async def delete_service_type(service_type_id: int, db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(
            select(ServiceType).where(ServiceType.id == service_type_id)
        )
        service_type = result.scalars().one_or_none()
        if service_type is None:
            raise HTTPException(status_code=404, detail="ServiceType not found")

        await db.delete(service_type)
        await db.commit()
        return ServiceTypeInDBBase.from_orm(service_type)
    except Exception as e:
        print(f"Ошибка удаления вида услуг: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to delete service_type: {str(e)}")


@router.patch("/{service_type_id}", response_model=ServiceTypeInDBBase)
async def update_service_type(service_type_id: int, service_type_update: ServiceTypeUpdate, db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(
            select(ServiceType).where(ServiceType.id == service_type_id)
        )
        existing_service_type = result.scalars().one_or_none()

        if existing_service_type is None:
            raise HTTPException(status_code=404, detail="ServiceType not found")

        for key, value in service_type_update.dict(exclude_unset=True).items():
            setattr(existing_service_type, key, value)

        await db.commit()
        await db.refresh(existing_service_type)
        return ServiceTypeInDBBase.from_orm(existing_service_type)
    except Exception as e:
        print(f"Ошибка частичного обновления вида услуг: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to update service_type: {str(e)}")
# endregion
