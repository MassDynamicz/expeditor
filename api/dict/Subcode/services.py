from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from fastapi import Depends
from config.db import get_db
from sqlalchemy.future import select
from .models import Subcode
from .schemas import SubcodeBase, SubcodeInDB


def obj_meta(obj):
    return {
        "id": {"label": "ID", "value": obj.id},
        "name": {"label": "Наименование", "value": obj.name},
        "owner": {"label": "Владелец", "data": obj.owner if obj.owner else None}
    }


class SubcodeService:
    async def get_list(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
        result = await db.execute(select(Subcode).
                                  options(joinedload(Subcode.owner)).
                                  offset(skip).limit(limit))
        objs = result.scalars().all()
        r_object = [obj_meta(obj) for obj in objs]
        return r_object

    async def get_object(obj_id: int, db: AsyncSession = Depends(get_db)):
        result = await db.execute(select(Subcode).
                                  options(joinedload(Subcode.owner)).
                                  where(Subcode.id == obj_id))
        obj = result.scalars().one_or_none()
        if obj is None:
            return None
        return obj_meta(obj)

    async def create_object(obj_schema: SubcodeBase, db: AsyncSession = Depends(get_db)):
        new_obj = Subcode(**obj_schema.dict())
        db.add(new_obj)
        await db.commit()
        await db.refresh(new_obj)
        return new_obj

    async def delete_object(obj_id: int, db: AsyncSession = Depends(get_db)):
        result = await db.execute(select(Subcode).where(Subcode.id == obj_id))
        obj = result.scalars().one_or_none()
        await db.delete(obj)
        await db.commit()

    async def update_object(obj_id: int, obj_schema: SubcodeInDB, db: AsyncSession = Depends(get_db)):
        result = await db.execute(select(Subcode).where(Subcode.id == obj_id))
        obj = result.scalars().one_or_none()
        if obj is None:
            return None
        for key, value in obj_schema.dict(exclude_unset=True).items():
            setattr(obj, key, value)
        await db.commit()
        await db.refresh(obj)
        return obj
