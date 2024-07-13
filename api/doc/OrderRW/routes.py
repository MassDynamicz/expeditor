from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from config.db import get_db
from api.doc.OrderRW.models import OrderRW
from api.doc.OrderRW.schemas import OrderRWInDBBase, OrderRWRelate, OrderRWCreate, OrderRWUpdate
from typing import List
from api.dict.Organization.schemas import OrganizationRelate
from api.auth.schemas import User
from api.dict.ServiceType.schemas import ServiceTypeInDBBase
from api.dict.Contract.schemas import ContractInDBBase
from api.dict.Contractor.schemas import ContractorInDBBase


router = APIRouter()


# Список
@router.get("/", response_model=List[OrderRWRelate])
async def read_orderrws(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(OrderRW)
        .options(
            selectinload(OrderRW.organization),
            selectinload(OrderRW.author),
            selectinload(OrderRW.manager),
            selectinload(OrderRW.client),
            selectinload(OrderRW.contract),
            selectinload(OrderRW.service_type)
        )
        .offset(skip).limit(limit)
    )
    orderrws = result.scalars().all()

    for orderrw in orderrws:
        if orderrw.organization:
            orderrw.organization_data = OrganizationRelate.from_orm(orderrw.organization)
        if orderrw.author:
            orderrw.author_data = User.from_orm(orderrw.author)
        if orderrw.manager:
            orderrw.manager_data = User.from_orm(orderrw.manager)
        if orderrw.client:
            orderrw.client_data = ContractorInDBBase.from_orm(orderrw.client)
        if orderrw.contract:
            orderrw.contract_data = ContractInDBBase.from_orm(orderrw.contract)
        if orderrw.service_type:
            orderrw.service_type_data = ServiceTypeInDBBase.from_orm(orderrw.service_type)

    return orderrws


@router.get("/{orderrw_id}", response_model=OrderRWRelate)
async def read_orderrw(orderrw_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(OrderRW)
        .options(
            selectinload(OrderRW.organization),
            selectinload(OrderRW.author),
            selectinload(OrderRW.manager),
            selectinload(OrderRW.client),
            selectinload(OrderRW.contract),
            selectinload(OrderRW.service_type)
        )
        .where(OrderRW.id == orderrw_id)
    )
    orderrw = result.scalars().one_or_none()
    if orderrw is None:
        raise HTTPException(status_code=404, detail="OrderRW not found")

    if orderrw.organization:
        orderrw.organization_data = OrganizationRelate.from_orm(orderrw.organization)
    if orderrw.author:
        orderrw.author_data = User.from_orm(orderrw.author)
    if orderrw.manager:
        orderrw.manager_data = User.from_orm(orderrw.manager)
    if orderrw.client:
        orderrw.client_data = ContractorInDBBase.from_orm(orderrw.client)
    if orderrw.contract:
        orderrw.contract_data = ContractInDBBase.from_orm(orderrw.contract)
    if orderrw.service_type:
        orderrw.service_type_data = ServiceTypeInDBBase.from_orm(orderrw.service_type)

    return OrderRWRelate.from_orm(orderrw)


@router.post("/", response_model=OrderRWInDBBase)
async def create_or_update_orderrw(orderrw: OrderRWCreate, db: AsyncSession = Depends(get_db)):
    try:
        # Создаем новую запись
        new_orderrw = OrderRW(**orderrw.dict())
        db.add(new_orderrw)
        await db.commit()
        await db.refresh(new_orderrw)
        return OrderRWInDBBase.from_orm(new_orderrw)
    except Exception as e:
        print(f"Ошибка создания или обновления заявки: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to create or update order rw: {str(e)}")
#
#
# @router.delete("/{orderrw_id}", response_model=OrderRWInDBBase)
# async def delete_orderrw(orderrw_id: int, db: AsyncSession = Depends(get_db)):
#     try:
#         result = await db.execute(
#             select(OrderRW).where(OrderRW.id == orderrw_id)
#         )
#         orderrw = result.scalars().one_or_none()
#         if orderrw is None:
#             raise HTTPException(status_code=404, detail="OrderRW not found")
#
#         await db.delete(orderrw)
#         await db.commit()
#         return OrderRWInDBBase.from_orm(orderrw)
#     except Exception as e:
#         print(f"Ошибка удаления договоров: {str(e)}")
#         raise HTTPException(status_code=500, detail=f"Failed to delete orderrw: {str(e)}")
#
#
# @router.patch("/{orderrw_id}", response_model=OrderRWInDBBase)
# async def update_orderrw(orderrw_id: int, orderrw_update: OrderRWUpdate, db: AsyncSession = Depends(get_db)):
#     try:
#         result = await db.execute(
#             select(OrderRW).where(OrderRW.id == orderrw_id)
#         )
#         existing_orderrw = result.scalars().one_or_none()
#
#         if existing_orderrw is None:
#             raise HTTPException(status_code=404, detail="OrderRW not found")
#
#         for key, value in orderrw_update.dict(exclude_unset=True).items():
#             setattr(existing_orderrw, key, value)
#
#         await db.commit()
#         await db.refresh(existing_orderrw)
#         return OrderRWInDBBase.from_orm(existing_orderrw)
#     except Exception as e:
#         print(f"Ошибка частичного обновления договоров: {str(e)}")
#         raise HTTPException(status_code=500, detail=f"Failed to update orderrw: {str(e)}")
