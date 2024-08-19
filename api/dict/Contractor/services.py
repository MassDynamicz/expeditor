from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from sqlalchemy.orm import joinedload
from config.db import get_db
from sqlalchemy.future import select
from .models import Contractor
from .schemas import ContractorBase, ContractorInDB


def obj_meta(obj):
    return {
        "id": {"label": "ID", "value": obj.id},
        "name": {"label": "Наименование", "value": obj.name},
        "guid": {"label": "УИ", "value": obj.guid},
        "full_name": {"label": "Полное наименование", "value": obj.full_name},
        "bin": {"label": "БИН/ИИН", "value": obj.bin},
        "kbe": {"label": "Кбе", "value": obj.kbe},
        "enterpreneur": {"label": "Является ИП", "value": obj.enterpreneur},
        "legal_address": {"label": "Юр. адрес", "value": obj.legal_address},
        "legal_entity": {"label": "Юр. лицо", "value": obj.legal_entity},
        "country_id": {"label": "country_id", "value": obj.country_id},
        "country": {"label": "Страна", "value": obj.country.name}
    }


class ContractorService:
    async def get_list(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
        result = await db.execute(select(Contractor).options(joinedload(Contractor.country)).offset(skip).limit(limit))
        objs = result.scalars().all()
        r_object = [obj_meta(obj) for obj in objs]
        return r_object

    async def get_object(obj_id: int, db: AsyncSession = Depends(get_db)):
        result = await db.execute(select(Contractor).options(joinedload(Contractor.country)).where(Contractor.id == obj_id))
        obj = result.scalars().one_or_none()
        if obj is None:
            return None
        return obj_meta(obj)

    async def create_object(obj_schema: ContractorBase, db: AsyncSession = Depends(get_db)):
        new_obj = Contractor(**obj_schema.dict())
        db.add(new_obj)
        await db.commit()
        await db.refresh(new_obj)
        return new_obj

    async def delete_object(obj_id: int, db: AsyncSession = Depends(get_db)):
        result = await db.execute(select(Contractor).where(Contractor.id == obj_id))
        obj = result.scalars().one_or_none()
        await db.delete(obj)
        await db.commit()

    async def update_object(obj_id: int, obj_schema: ContractorInDB, db: AsyncSession = Depends(get_db)):
        result = await db.execute(select(Contractor).where(Contractor.id == obj_id))
        obj = result.scalars().one_or_none()
        if obj is None:
            return None
        for key, value in obj_schema.dict(exclude_unset=True).items():
            setattr(obj, key, value)
        await db.commit()
        await db.refresh(obj)
        return obj
