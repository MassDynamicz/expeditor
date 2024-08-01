from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from config.db import get_db
from typing import List
from .schemas import OrderRailWayInDB, OrderRailWayBase
from .services import OrderRailWayService

router = APIRouter()


@router.get("/", response_model=List[OrderRailWayInDB])
async def get_objs(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
    try:
        orders = await OrderRailWayService.get_list(skip, limit, db)
        return [OrderRailWayInDB.from_orm(order) for order in orders]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to read orders rail way: {str(e)}")


@router.get("/{obj_id}", response_model=OrderRailWayInDB)
async def get_obj(obj_id: int, db: AsyncSession = Depends(get_db)):
    try:
        order = await OrderRailWayService.get_object(obj_id, db)
        if order is None:
            raise HTTPException(status_code=404, detail="Order rail way not found")
        return OrderRailWayInDB.from_orm(order)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to read order rail way: {str(e)}")


@router.post("/", response_model=OrderRailWayBase)
async def create_obj(order: OrderRailWayBase, db: AsyncSession = Depends(get_db)):
    try:
        new_order = await OrderRailWayService.create_object(order, db)
        return OrderRailWayInDB.from_orm(new_order)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create order rail way: {str(e)}")