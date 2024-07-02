from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from api.dict.Container.schemas import ContainerRelate, ContainerCreate, ContainerUpdate, ContainerInDBBase
from api.dict.WagonType.schemas import WagonTypeInDBBase
from config.db import get_db
from api.dict.Container.models import Container
from typing import List


router = APIRouter()


# region РОУТ
@router.get("/", response_model=List[ContainerRelate])
async def read_containers(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(
            select(Container)
            .options(selectinload(Container.wagon_type))
            .offset(skip).limit(limit)
        )
        containers = result.scalars().all()

        for container in containers:
            if container.wagon_type:
                container.wagon_type_data = WagonTypeInDBBase.from_orm(container.wagon_type)

        return [ContainerRelate.from_orm(container) for container in containers]
    except Exception as e:
        print(f"Ошибка чтения контейнера: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to read container: {str(e)}")


# контейнера по идентификатору
@router.get("/{container_id}", response_model=ContainerRelate)
async def read_container(container_id: int, db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(
            select(Container).options(selectinload(Container.wagon_type)).where(Container.id == container_id)
        )
        container = result.scalars().one_or_none()
        if container is None:
            raise HTTPException(status_code=404, detail="Container not found")

        if container.wagon_type:
            container.wagon_type_data = WagonTypeInDBBase.from_orm(container.wagon_type)

        return ContainerRelate.from_orm(container)
    except Exception as e:
        print(f"Ошибка чтения контейнера: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to read container: {str(e)}")


# Создание новой контейнера или обновление существующей
@router.post("/", response_model=ContainerInDBBase)
async def create_or_update_container(container: ContainerCreate, db: AsyncSession = Depends(get_db)):
    try:
        # Создаем новую запись
        new_container = Container(**container.dict())
        db.add(new_container)
        await db.commit()
        await db.refresh(new_container)
        return ContainerInDBBase.from_orm(new_container)
    except Exception as e:
        print(f"Ошибка создания или обновления контейнера: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to create or update VAT: {str(e)}")


# Удаление контейнера по идентификатору
@router.delete("/{container_id}", response_model=ContainerInDBBase)
async def delete_container(container_id: int, db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(
            select(Container).where(Container.id == container_id)
        )
        container = result.scalars().one_or_none()
        if container is None:
            raise HTTPException(status_code=404, detail="Container not found")

        await db.delete(container)
        await db.commit()
        return ContainerInDBBase.from_orm(container)
    except Exception as e:
        print(f"Ошибка удаления контейнера: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to delete container: {str(e)}")


# Частичное обновление контейнера
@router.patch("/{container_id}", response_model=ContainerInDBBase)
async def update_container(container_id: int, container_update: ContainerUpdate, db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(
            select(Container).where(Container.id == container_id)
        )
        existing_container = result.scalars().one_or_none()

        if existing_container is None:
            raise HTTPException(status_code=404, detail="Container not found")

        for key, value in container_update.dict(exclude_unset=True).items():
            setattr(existing_container, key, value)

        await db.commit()
        await db.refresh(existing_container)
        return ContainerInDBBase.from_orm(existing_container)
    except Exception as e:
        print(f"Ошибка частичного обновления контейнера: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to update container: {str(e)}")
# endregion
