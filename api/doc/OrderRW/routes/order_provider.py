from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from typing import List
from api.dict.Contract.schemas import ContractInDBBase
from api.dict.Contractor.schemas import ContractorInDBBase
from api.dict.Currency.schemas import CurrencyInDBBase
from api.dict.Operation.schemas import OperationInDBBase
from api.dict.Vat.schemas import VatInDBBase
from config.db import get_db
from api.doc.OrderRW.models import OrderRW_Provider
from api.doc.OrderRW.schemas import ORWProviderRead, ORWProviderCreate, ORWProviderUpdate, ORWProvider_id

router = APIRouter()


@router.get("/", response_model=List[ORWProviderRead])
async def read_order_providers(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(OrderRW_Provider).options(*get_obj_options()).offset(skip).limit(limit))
    order_providers = result.scalars().all()
    for orderrw_provider in order_providers:
        add_related_data(orderrw_provider)
    return order_providers


@router.get("/{obj_id}", response_model=ORWProviderRead)
async def read_order_provider(obj_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(OrderRW_Provider).options(*get_obj_options()).where(OrderRW_Provider.id == obj_id))
    provider = result.scalars().one_or_none()
    if provider is None:
        raise HTTPException(status_code=404, detail="Provider not found")
    add_related_data(provider)
    return ORWProviderRead.from_orm(provider)


@router.post("/", response_model=ORWProviderCreate)
async def create_order_provider(orderrw: ORWProviderCreate, db: AsyncSession = Depends(get_db)):
    try:
        new_orderrw = OrderRW_Provider(**orderrw.dict())
        db.add(new_orderrw)
        await db.commit()
        await db.refresh(new_orderrw)
        return ORWProviderCreate.from_orm(new_orderrw)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create provider: {str(e)}")


@router.patch("/{obj_id}", response_model=ORWProviderUpdate)
async def update_order_provider(obj_id: int, orderrw_update: ORWProviderUpdate, db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(select(OrderRW_Provider).where(OrderRW_Provider.id == obj_id))
        existing_orderrw = result.scalars().one_or_none()
        if existing_orderrw is None:
            raise HTTPException(status_code=404, detail="Provider not found")
        for key, value in orderrw_update.dict(exclude_unset=True).items():
            setattr(existing_orderrw, key, value)
        await db.commit()
        await db.refresh(existing_orderrw)
        return ORWProviderUpdate.from_orm(existing_orderrw)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update provider: {str(e)}")


@router.delete("/{obj_id}", response_model=ORWProvider_id)
async def delete_order_provider(obj_id: int, db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(select(OrderRW_Provider).where(OrderRW_Provider.id == obj_id))
        orderrw = result.scalars().one_or_none()
        if orderrw is None:
            raise HTTPException(status_code=404, detail="Provider not found")
        await db.delete(orderrw)
        await db.commit()
        return ORWProvider_id.from_orm(orderrw)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete provider: {str(e)}")


def get_obj_options():
    return [
        selectinload(OrderRW_Provider.provider),
        selectinload(OrderRW_Provider.contract),
        selectinload(OrderRW_Provider.currency),
        selectinload(OrderRW_Provider.operation),
        selectinload(OrderRW_Provider.vat)
    ]


def add_related_data(orderrw_provider):
    if orderrw_provider.provider:
        orderrw_provider.provider_data = ContractorInDBBase.from_orm(orderrw_provider.provider)
    if orderrw_provider.contract:
        orderrw_provider.contract_data = ContractInDBBase.from_orm(orderrw_provider.contract)
    if orderrw_provider.currency:
        orderrw_provider.currency_data = CurrencyInDBBase.from_orm(orderrw_provider.currency)
    if orderrw_provider.operation:
        orderrw_provider.operation_data = OperationInDBBase.from_orm(orderrw_provider.operation)
    if orderrw_provider.vat:
        orderrw_provider.vat_data = VatInDBBase.from_orm(orderrw_provider.vat)
