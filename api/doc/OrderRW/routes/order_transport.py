from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from typing import List

from api.dict.Container.schemas import ContainerInDBBase
from api.dict.Etsng.schemas import EtsngInDBBase
from api.dict.Gng.schemas import GngInDBBase
from api.dict.Station.schemas import StationInDBBase
from api.dict.Subcode.schemas import SubcodeInDBBase
from api.dict.Vat.schemas import VatInDBBase
from api.dict.Wagon.schemas import WagonInDBBase
from api.dict.WagonType.schemas import WagonTypeInDBBase
from config.db import get_db
from api.doc.OrderRW.models import OrderRW_Transport
from api.doc.OrderRW.schemas import ORWTransportRead, ORWTransportCreate, ORWTransportUpdate, ORWTransport_id

router = APIRouter()


@router.get("/", response_model=List[ORWTransportRead])
async def read_order_transports(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(OrderRW_Transport).options(*get_obj_options()).offset(skip).limit(limit))
    order_tr = result.scalars().all()
    for orderrw_tr in order_tr:
        add_related_data(orderrw_tr)
    return order_tr


@router.get("/{obj_id}", response_model=ORWTransportRead)
async def read_order_transport(obj_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(OrderRW_Transport).options(*get_obj_options()).where(OrderRW_Transport.id == obj_id))
    transport = result.scalars().one_or_none()
    if transport is None:
        raise HTTPException(status_code=404, detail="Transport not found")
    add_related_data(transport)
    return ORWTransportRead.from_orm(transport)


@router.post("/", response_model=ORWTransportCreate)
async def create_order_transport(orderrw: ORWTransportCreate, db: AsyncSession = Depends(get_db)):
    try:
        new_orderrw = OrderRW_Transport(**orderrw.dict())
        db.add(new_orderrw)
        await db.commit()
        await db.refresh(new_orderrw)
        return ORWTransportCreate.from_orm(new_orderrw)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create transport: {str(e)}")


@router.patch("/{obj_id}", response_model=ORWTransportUpdate)
async def update_order_transport(obj_id: int, orderrw_update: ORWTransportUpdate, db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(select(OrderRW_Transport).where(OrderRW_Transport.id == obj_id))
        existing_orderrw = result.scalars().one_or_none()
        if existing_orderrw is None:
            raise HTTPException(status_code=404, detail="Transport not found")
        for key, value in orderrw_update.dict(exclude_unset=True).items():
            setattr(existing_orderrw, key, value)
        await db.commit()
        await db.refresh(existing_orderrw)
        return ORWTransportUpdate.from_orm(existing_orderrw)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update transport: {str(e)}")


@router.delete("/{obj_id}", response_model=ORWTransport_id)
async def delete_order_transport(obj_id: int, db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(select(OrderRW_Transport).where(OrderRW_Transport.id == obj_id))
        orderrw = result.scalars().one_or_none()
        if orderrw is None:
            raise HTTPException(status_code=404, detail="OrderRW route not found")
        await db.delete(orderrw)
        await db.commit()
        return ORWTransport_id.from_orm(orderrw)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete transport: {str(e)}")


def get_obj_options():
    return [
        selectinload(OrderRW_Transport.station_otpr),
        selectinload(OrderRW_Transport.station_nazn),
        selectinload(OrderRW_Transport.wagon),
        selectinload(OrderRW_Transport.wagon_cn),
        selectinload(OrderRW_Transport.container),
        selectinload(OrderRW_Transport.subcode1),
        selectinload(OrderRW_Transport.subcode2),
        selectinload(OrderRW_Transport.subcode3),
        selectinload(OrderRW_Transport.subcode4),
        selectinload(OrderRW_Transport.subcode5),
        selectinload(OrderRW_Transport.etsng),
        selectinload(OrderRW_Transport.gng),
        selectinload(OrderRW_Transport.wagon_type),
        selectinload(OrderRW_Transport.vat)
    ]


def add_related_data(orderrw_tr):
    if orderrw_tr.station_otpr:
        orderrw_tr.station_otpr_data = StationInDBBase.from_orm(orderrw_tr.station_otpr)
    if orderrw_tr.station_nazn:
        orderrw_tr.station_nazn_data = StationInDBBase.from_orm(orderrw_tr.station_nazn)
    if orderrw_tr.wagon:
        orderrw_tr.wagon_data = WagonInDBBase.from_orm(orderrw_tr.wagon)
    if orderrw_tr.wagon_cn:
        orderrw_tr.wagon_cn_data = WagonInDBBase.from_orm(orderrw_tr.wagon_cn)
    if orderrw_tr.container:
        orderrw_tr.container_data = ContainerInDBBase.from_orm(orderrw_tr.container)
    if orderrw_tr.subcode1:
        orderrw_tr.subcode1_data = SubcodeInDBBase.from_orm(orderrw_tr.subcode1)
    if orderrw_tr.subcode2:
        orderrw_tr.subcode2_data = SubcodeInDBBase.from_orm(orderrw_tr.subcode2)
    if orderrw_tr.subcode3:
        orderrw_tr.subcode3_data = SubcodeInDBBase.from_orm(orderrw_tr.subcode3)
    if orderrw_tr.subcode4:
        orderrw_tr.subcode4_data = SubcodeInDBBase.from_orm(orderrw_tr.subcode4)
    if orderrw_tr.subcode5:
        orderrw_tr.subcode5_data = SubcodeInDBBase.from_orm(orderrw_tr.subcode5)
    if orderrw_tr.wagon_type:
        orderrw_tr.wagon_type_data = WagonTypeInDBBase.from_orm(orderrw_tr.wagon_type)
    if orderrw_tr.etsng:
        orderrw_tr.etsng_data = EtsngInDBBase.from_orm(orderrw_tr.etsng)
    if orderrw_tr.gng:
        orderrw_tr.gng_data = GngInDBBase.from_orm(orderrw_tr.gng)
    if orderrw_tr.vat:
        orderrw_tr.vat_data = VatInDBBase.from_orm(orderrw_tr.vat)
