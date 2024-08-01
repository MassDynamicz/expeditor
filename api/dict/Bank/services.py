from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from config.db import get_db
from sqlalchemy.future import select
from .models import Bank
from .schemas import BankBase, BankInDB


class BankService:
    async def get_list(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
        result = await db.execute(select(Bank).offset(skip).limit(limit))
        objs = result.scalars().all()
        return objs

    async def get_object(obj_id: int, db: AsyncSession = Depends(get_db)):
        result = await db.execute(select(Bank).where(Bank.id == obj_id))
        obj = result.scalars().one_or_none()
        return obj

    async def create_object(obj_schema: BankBase, db: AsyncSession = Depends(get_db)):
        new_obj = Bank(**obj_schema.dict())
        db.add(new_obj)
        await db.commit()
        await db.refresh(new_obj)
        return new_obj

    async def delete_object(obj_id: int, db: AsyncSession = Depends(get_db)):
        result = await db.execute(select(Bank).where(Bank.id == obj_id))
        obj = result.scalars().one_or_none()
        await db.delete(obj)
        await db.commit()

    async def update_object(obj_id: int, obj_schema: BankInDB, db: AsyncSession = Depends(get_db)):
        result = await db.execute(select(Bank).where(Bank.id == obj_id))
        obj = result.scalars().one_or_none()
        if obj is None:
            return None
        for key, value in obj_schema.dict(exclude_unset=True).items():
            setattr(obj, key, value)
        await db.commit()
        await db.refresh(obj)
        return obj
