from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from fastapi import Depends
from config.db import get_db
from sqlalchemy.future import select
from .models import Operation
from .schemas import OperationBase, OperationInDB


def obj_meta(obj):
    return {
        "id": {"label": "ID", "value": obj.id},
        "name": {"label": "Наименование", "value": obj.name},
        "code": {"label": "Код операции", "value": obj.code},
        "vat_id": {"label": "vat_id", "value": obj.vat_id},
        "vat": {"label": "Ставка НДС", "value": obj.vat.name if obj.vat else None}
    }


class OperationService:
    async def get_list(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
        result = await db.execute(select(Operation).options(joinedload(Operation.vat)).offset(skip).limit(limit))
        objs = result.scalars().all()
        r_object = [obj_meta(obj) for obj in objs]
        return r_object

    async def get_object(obj_id: int, db: AsyncSession = Depends(get_db)):
        result = await db.execute(select(Operation).options(joinedload(Operation.vat)).where(Operation.id == obj_id))
        obj = result.scalars().one_or_none()
        if obj is None:
            return None
        return obj_meta(obj)

    async def create_object(obj_schema: OperationBase, db: AsyncSession = Depends(get_db)):
        new_obj = Operation(**obj_schema.dict())
        db.add(new_obj)
        await db.commit()
        await db.refresh(new_obj)
        return new_obj

    async def delete_object(obj_id: int, db: AsyncSession = Depends(get_db)):
        result = await db.execute(select(Operation).where(Operation.id == obj_id))
        obj = result.scalars().one_or_none()
        await db.delete(obj)
        await db.commit()

    async def update_object(obj_id: int, obj_schema: OperationInDB, db: AsyncSession = Depends(get_db)):
        result = await db.execute(select(Operation).where(Operation.id == obj_id))
        obj = result.scalars().one_or_none()
        if obj is None:
            return None
        for key, value in obj_schema.dict(exclude_unset=True).items():
            setattr(obj, key, value)
        await db.commit()
        await db.refresh(obj)
        return obj
