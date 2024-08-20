from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from sqlalchemy.orm import joinedload
from config.db import get_db
from sqlalchemy.future import select
from .models import Contract
from .schemas import ContractBase, ContractInDB


def obj_meta(obj):
    return {
        "id": {"label": "ID", "value": obj.id},
        "name": {"label": "Наименование", "value": obj.name},
        "guid": {"label": "УИ", "value": obj.guid},
        "number": {"label": "Номер", "value": obj.number},
        "from_date": {"label": "Дата начала", "value": obj.from_date},
        "to_date": {"label": "Дата окончания", "value": obj.to_date},
        "organization": {"label": "Организация", "data": obj.organization},
        "contractor": {"label": "Контрагент", "data": obj.contractor},
        "currency": {"label": "Валюта взаиморасчетов", "data": obj.currency}
    }


class ContractService:
    async def get_list(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
        result = await db.execute(select(Contract)
                                  .options(joinedload(Contract.organization))
                                  .options(joinedload(Contract.contractor))
                                  .options(joinedload(Contract.currency))
                                  .offset(skip).limit(limit))
        objs = result.scalars().all()
        r_object = [obj_meta(obj) for obj in objs]
        return r_object

    async def get_object(obj_id: int, db: AsyncSession = Depends(get_db)):
        result = await db.execute(select(Contract)
                                  .options(joinedload(Contract.organization))
                                  .options(joinedload(Contract.contractor))
                                  .options(joinedload(Contract.currency))
                                  .where(Contract.id == obj_id))
        obj = result.scalars().one_or_none()
        if obj is None:
            return None
        return obj_meta(obj)

    async def create_object(obj_schema: ContractBase, db: AsyncSession = Depends(get_db)):
        new_obj = Contract(**obj_schema.dict())
        db.add(new_obj)
        await db.commit()
        await db.refresh(new_obj)
        return new_obj

    async def delete_object(obj_id: int, db: AsyncSession = Depends(get_db)):
        result = await db.execute(select(Contract).where(Contract.id == obj_id))
        obj = result.scalars().one_or_none()
        await db.delete(obj)
        await db.commit()

    async def update_object(obj_id: int, obj_schema: ContractInDB, db: AsyncSession = Depends(get_db)):
        result = await db.execute(select(Contract).where(Contract.id == obj_id))
        obj = result.scalars().one_or_none()
        if obj is None:
            return None
        for key, value in obj_schema.dict(exclude_unset=True).items():
            setattr(obj, key, value)
        await db.commit()
        await db.refresh(obj)
        return obj
