from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from config.db import get_db
from sqlalchemy.future import select
from .models import Organization
from .schemas import OrganizationBase


class OrganizationService:
    async def get_list(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
        result = await db.execute(select(Organization).offset(skip).limit(limit))
        objs = result.scalars().all()
        return objs

    async def get_object(obj_id: int, db: AsyncSession = Depends(get_db)):
        result = await db.execute(select(Organization).where(Organization.id == obj_id))
        obj = result.scalars().one_or_none()
        return obj

    async def create_object(obj_schema: OrganizationBase, db: AsyncSession = Depends(get_db)):
        new_obj = Organization(**obj_schema.dict())
        db.add(new_obj)
        await db.commit()
        await db.refresh(new_obj)
        return new_obj
