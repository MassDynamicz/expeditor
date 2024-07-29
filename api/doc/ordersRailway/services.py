from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from config.db import get_db
from sqlalchemy.future import select
from api.doc.ordersRailway.models import OrderRailWay
from api.doc.ordersRailway.schemas import OrderRailWayBase, OrderRailWayInDB


class OrderRailWayService:
    async def get_list(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
        result = await db.execute(select(OrderRailWay).offset(skip).limit(limit))
        orders = result.scalars().all()
        return orders

    async def get_object(obj_id: int, db: AsyncSession = Depends(get_db)):
        result = await db.execute(select(OrderRailWay).where(OrderRailWay.id == obj_id))
        order = result.scalars().one_or_none()
        return order

    async def create_object(obj_schema: OrderRailWayBase, db: AsyncSession = Depends(get_db)):
        new_order = OrderRailWay(**obj_schema.dict())
        db.add(new_order)
        await db.commit()
        await db.refresh(new_order)
        return new_order