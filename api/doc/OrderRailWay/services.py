from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from sqlalchemy.orm import joinedload, selectinload
from config.db import get_db
from sqlalchemy.future import select
from .models import OrderRailWay
from .schemas import OrderRailWayBase, OrderRailWayInDB
from ..OrderRailWayRoute.models import OrderRailWayRoute
from ...dict.Contract.models import Contract


def obj_meta(obj):
    return {
        "id": {"label": "ID", "value": obj.id},
        "date": {"label": "Дата", "value": obj.date},
        "created_at": {"label": "Дата создания", "value": obj.created_at},
        "updated_at": {"label": "Дата последнего обновления", "value": obj.updated_at},
        "comment": {"label": "Комментарий", "value": obj.comment},
        "sum": {"label": "Сумма", "value": obj.sum},
        "amount": {"label": "Количество", "value": obj.amount},
        "rate": {"label": "Курс", "value": obj.rate},
        "confirmed": {"label": "Подтверждена", "value": obj.confirmed},
        "organization": {"label": "Организация", "data": obj.organization},
        "author": {"label": "Автор", "data": obj.author},
        "manager": {"label": "Ответственный", "data": obj.manager},
        "client": {"label": "Клиент", "data": obj.client},
        "contract": {"label": "Договор", "data": obj.contract},
        "service_type": {"label": "Вид услуги", "data": obj.service_type},
        "order_railway_routes": {"label": "Маршруты", "data": obj.order_railway_routes if obj.order_railway_routes else None}
    }


class OrderRailWayService:
    async def get_list(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
        result = await db.execute(select(OrderRailWay)
                                  .options(joinedload(OrderRailWay.organization))
                                  .options(joinedload(OrderRailWay.author))
                                  .options(joinedload(OrderRailWay.manager))
                                  .options(joinedload(OrderRailWay.client))
                                  .options(joinedload(OrderRailWay.contract).joinedload(Contract.currency))
                                  .options(joinedload(OrderRailWay.service_type))
                                  .options(selectinload(OrderRailWay.order_railway_routes)
                                           .joinedload(OrderRailWayRoute.vat))
                                  .options(selectinload(OrderRailWay.order_railway_routes)
                                           .joinedload(OrderRailWayRoute.station_otpr))
                                  .options(selectinload(OrderRailWay.order_railway_routes)
                                           .joinedload(OrderRailWayRoute.station_nazn))
                                  .options(selectinload(OrderRailWay.order_railway_routes)
                                           .joinedload(OrderRailWayRoute.wagon_type))
                                  .options(selectinload(OrderRailWay.order_railway_routes)
                                           .joinedload(OrderRailWayRoute.etsng))
                                  .options(selectinload(OrderRailWay.order_railway_routes)
                                           .joinedload(OrderRailWayRoute.gng))
                                  .offset(skip).limit(limit))
        objs = result.scalars().all()
        r_object = [obj_meta(obj) for obj in objs]
        return r_object

    async def get_object(obj_id: int, db: AsyncSession = Depends(get_db)):
        result = await db.execute(select(OrderRailWay)
                                  .options(joinedload(OrderRailWay.organization))
                                  .options(joinedload(OrderRailWay.author))
                                  .options(joinedload(OrderRailWay.manager))
                                  .options(joinedload(OrderRailWay.client))
                                  .options(joinedload(OrderRailWay.contract))
                                  .options(joinedload(OrderRailWay.service_type))
                                  .options(selectinload(OrderRailWay.order_railway_routes)
                                           .joinedload(OrderRailWayRoute.vat))
                                  .options(selectinload(OrderRailWay.order_railway_routes)
                                           .joinedload(OrderRailWayRoute.station_otpr))
                                  .options(selectinload(OrderRailWay.order_railway_routes)
                                           .joinedload(OrderRailWayRoute.station_nazn))
                                  .options(selectinload(OrderRailWay.order_railway_routes)
                                           .joinedload(OrderRailWayRoute.wagon_type))
                                  .options(selectinload(OrderRailWay.order_railway_routes)
                                           .joinedload(OrderRailWayRoute.etsng))
                                  .options(selectinload(OrderRailWay.order_railway_routes)
                                           .joinedload(OrderRailWayRoute.gng))
                                  .where(OrderRailWay.id == obj_id))
        obj = result.scalars().one_or_none()
        if obj is None:
            return None
        return obj_meta(obj)

    async def create_object(obj_schema: OrderRailWayBase, db: AsyncSession = Depends(get_db)):
        new_obj = OrderRailWay(**obj_schema.dict())
        db.add(new_obj)
        await db.commit()
        await db.refresh(new_obj)
        return new_obj

    async def delete_object(obj_id: int, db: AsyncSession = Depends(get_db)):
        result = await db.execute(select(OrderRailWay).where(OrderRailWay.id == obj_id))
        obj = result.scalars().one_or_none()
        await db.delete(obj)
        await db.commit()

    async def update_object(obj_id: int, obj_schema: OrderRailWayInDB, db: AsyncSession = Depends(get_db)):
        result = await db.execute(select(OrderRailWay).where(OrderRailWay.id == obj_id))
        obj = result.scalars().one_or_none()
        if obj is None:
            return None
        for key, value in obj_schema.dict(exclude_unset=True).items():
            setattr(obj, key, value)
        await db.commit()
        await db.refresh(obj)
        return obj
