from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from fastapi import Depends
from config.db import get_db
from sqlalchemy.future import select
from .models import Wagon
from .schemas import WagonBase, WagonInDB


def obj_meta(obj):
    return {
        "id": {"label": "ID", "value": obj.id},
        "name": {"label": "Номер вагона", "value": obj.name},
        "wagon_type_id": {"label": "wagon_type_id", "value": obj.wagon_type_id},
        "wagon_type": {"label": "Род ПС", "value": obj.wagon_type.name if obj.wagon_type else None}
    }


class WagonService:
    async def get_list(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
        result = await db.execute(select(Wagon).options(joinedload(Wagon.wagon_type)).offset(skip).limit(limit))
        objs = result.scalars().all()
        r_object = [obj_meta(obj) for obj in objs]
        return r_object

    async def get_object(obj_id: int, db: AsyncSession = Depends(get_db)):
        result = await db.execute(select(Wagon).options(joinedload(Wagon.wagon_type)).where(Wagon.id == obj_id))
        obj = result.scalars().one_or_none()
        if obj is None:
            return None
        return obj_meta(obj)

    async def create_object(obj_schema: WagonBase, db: AsyncSession = Depends(get_db)):
        new_obj = Wagon(**obj_schema.dict())
        db.add(new_obj)
        await db.commit()
        await db.refresh(new_obj)
        return new_obj

    async def delete_object(obj_id: int, db: AsyncSession = Depends(get_db)):
        result = await db.execute(select(Wagon).where(Wagon.id == obj_id))
        obj = result.scalars().one_or_none()
        await db.delete(obj)
        await db.commit()

    async def update_object(obj_id: int, obj_schema: WagonInDB, db: AsyncSession = Depends(get_db)):
        result = await db.execute(select(Wagon).where(Wagon.id == obj_id))
        obj = result.scalars().one_or_none()
        if obj is None:
            return None
        for key, value in obj_schema.dict(exclude_unset=True).items():
            setattr(obj, key, value)
        await db.commit()
        await db.refresh(obj)
        return obj
