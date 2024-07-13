from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from typing import List
from api.dict.Etsng.schemas import EtsngInDBBase
from api.dict.Gng.schemas import GngInDBBase
from api.dict.Station.schemas import StationInDBBase
from api.dict.Vat.schemas import VatInDBBase
from api.dict.WagonType.schemas import WagonTypeInDBBase
from config.db import get_db
from api.doc.OrderRW.models import OrderRW_Route
from api.doc.OrderRW.schemas import ORWRouteRead, ORWRouteCreate, ORWRouteUpdate, ORWRoute_id, ORWBase

router = APIRouter()


@router.get("/", response_model=List[ORWRouteRead])
async def read_orderrwroute(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(OrderRW_Route).options(*get_obj_options()).offset(skip).limit(limit))
    orderrwroutes = result.scalars().all()
    for orderrw in orderrwroutes:
        add_related_data(orderrw)
    return orderrwroutes


@router.get("/{obj_id}", response_model=ORWRouteRead)
async def read_orderrwroute(obj_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(OrderRW_Route).options(*get_obj_options()).where(OrderRW_Route.id == obj_id))
    orderrw = result.scalars().one_or_none()
    if orderrw is None:
        raise HTTPException(status_code=404, detail="OrderRW route not found")
    add_related_data(orderrw)
    return ORWRouteRead.from_orm(orderrw)


@router.post("/", response_model=ORWRouteCreate)
async def create_orderrwroute(orderrw: ORWRouteCreate, db: AsyncSession = Depends(get_db)):
    try:
        new_orderrw = OrderRW_Route(**orderrw.dict())
        db.add(new_orderrw)
        await db.commit()
        await db.refresh(new_orderrw)
        return ORWRouteCreate.from_orm(new_orderrw)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create order rw route: {str(e)}")


@router.patch("/{obj_id}", response_model=ORWRouteUpdate)
async def update_orderrw(obj_id: int, orderrw_update: ORWRouteUpdate, db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(select(OrderRW_Route).where(OrderRW_Route.id == obj_id))
        existing_orderrw = result.scalars().one_or_none()
        if existing_orderrw is None:
            raise HTTPException(status_code=404, detail="OrderRW route not found")
        for key, value in orderrw_update.dict(exclude_unset=True).items():
            setattr(existing_orderrw, key, value)
        await db.commit()
        await db.refresh(existing_orderrw)
        return ORWRouteUpdate.from_orm(existing_orderrw)
    except Exception as e:
        print(f"Ошибка частичного обновления заявки: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to update order rw route: {str(e)}")


@router.delete("/{obj_id}", response_model=ORWRoute_id)
async def delete_orderrw(obj_id: int, db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(select(OrderRW_Route).where(OrderRW_Route.id == obj_id))
        orderrw = result.scalars().one_or_none()
        if orderrw is None:
            raise HTTPException(status_code=404, detail="OrderRW route not found")
        await db.delete(orderrw)
        await db.commit()
        return ORWRoute_id.from_orm(orderrw)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete order rw route: {str(e)}")


def get_obj_options():
    return [
        selectinload(OrderRW_Route.orderrw),
        selectinload(OrderRW_Route.station_otpr),
        selectinload(OrderRW_Route.station_nazn),
        selectinload(OrderRW_Route.wagon_type),
        selectinload(OrderRW_Route.etsng),
        selectinload(OrderRW_Route.gng),
        selectinload(OrderRW_Route.vat)
    ]


def add_related_data(orderrw):
    if orderrw.orderrw:
        orderrw.orderrw_data = ORWBase.from_orm(orderrw.orderrw)
    if orderrw.station_otpr:
        orderrw.station_otpr_data = StationInDBBase.from_orm(orderrw.station_otpr)
    if orderrw.station_nazn:
        orderrw.station_nazn_data = StationInDBBase.from_orm(orderrw.station_nazn)
    if orderrw.wagon_type:
        orderrw.wagon_type_data = WagonTypeInDBBase.from_orm(orderrw.wagon_type)
    if orderrw.etsng:
        orderrw.etsng_data = EtsngInDBBase.from_orm(orderrw.etsng)
    if orderrw.gng:
        orderrw.gng_data = GngInDBBase.from_orm(orderrw.gng)
    if orderrw.vat:
        orderrw.vat_data = VatInDBBase.from_orm(orderrw.vat)
