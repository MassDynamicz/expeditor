from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from sqlalchemy.orm import joinedload
from config.db import get_db
from sqlalchemy.future import select
from .models import OrderRailWayRoute
from .schemas import OrderRailWayRouteBase, OrderRailWayRouteInDB
from ...dict.Contract.models import Contract


def obj_meta(obj):
    return {
        "id": {"label": "ID", "value": obj.id},
        "index": {"label": "Номер строки", "value": obj.index},
        "created_at": {"label": "Дата создания", "value": obj.created_at},
        "updated_at": {"label": "Дата последнего обновления", "value": obj.updated_at},
        "comment": {"label": "Комментарий", "value": obj.comment},
        "weight": {"label": "Вес (тн.)", "value": obj.weight},
        "amount": {"label": "Количество", "value": obj.amount},
        "price": {"label": "Цена", "value": obj.price},
        "sum": {"label": "Сумма", "value": obj.sum},
        "order": {"label": "Заявка", "data": obj.order},
        "station_otpr": {"label": "Станция отпр.", "data": obj.station_otpr},
        "station_nazn": {"label": "Станция назн.", "data": obj.station_nazn},
        "wagon_type": {"label": "Род ПС", "data": obj.wagon_type},
        "etsng": {"label": "ЕТСНГ", "data": obj.etsng},
        "gng": {"label": "ГНГ", "data": obj.gng},
        "vat": {"label": "НДС", "data": obj.vat}
    }


class OrderRailWayRouteService:
    async def get_list(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
        result = await db.execute(select(OrderRailWayRoute)
                                  .options(joinedload(OrderRailWayRoute.order))
                                  .options(joinedload(OrderRailWayRoute.station_otpr))
                                  .options(joinedload(OrderRailWayRoute.station_nazn))
                                  .options(joinedload(OrderRailWayRoute.wagon_type))
                                  .options(joinedload(OrderRailWayRoute.etsng))
                                  .options(joinedload(OrderRailWayRoute.gng))
                                  .options(joinedload(OrderRailWayRoute.vat))
                                  .offset(skip).limit(limit))
        objs = result.scalars().all()
        r_object = [obj_meta(obj) for obj in objs]
        return r_object

    async def get_object(obj_id: int, db: AsyncSession = Depends(get_db)):
        result = await db.execute(select(OrderRailWayRoute)
                                  .options(joinedload(OrderRailWayRoute.order))
                                  .options(joinedload(OrderRailWayRoute.station_otpr))
                                  .options(joinedload(OrderRailWayRoute.station_nazn))
                                  .options(joinedload(OrderRailWayRoute.wagon_type))
                                  .options(joinedload(OrderRailWayRoute.etsng))
                                  .options(joinedload(OrderRailWayRoute.gng))
                                  .options(joinedload(OrderRailWayRoute.vat))
                                  .where(OrderRailWayRoute.id == obj_id))
        obj = result.scalars().one_or_none()
        if obj is None:
            return None
        return obj_meta(obj)

    async def create_object(obj_schema: OrderRailWayRouteBase, db: AsyncSession = Depends(get_db)):
        new_obj = OrderRailWayRoute(**obj_schema.dict())
        db.add(new_obj)
        await db.commit()
        await db.refresh(new_obj)
        return new_obj

    async def delete_object(obj_id: int, db: AsyncSession = Depends(get_db)):
        result = await db.execute(select(OrderRailWayRoute).where(OrderRailWayRoute.id == obj_id))
        obj = result.scalars().one_or_none()
        await db.delete(obj)
        await db.commit()

    async def update_object(obj_id: int, obj_schema: OrderRailWayRouteInDB, db: AsyncSession = Depends(get_db)):
        result = await db.execute(select(OrderRailWayRoute).where(OrderRailWayRoute.id == obj_id))
        obj = result.scalars().one_or_none()
        if obj is None:
            return None
        for key, value in obj_schema.dict(exclude_unset=True).items():
            setattr(obj, key, value)
        await db.commit()
        await db.refresh(obj)
        return obj
