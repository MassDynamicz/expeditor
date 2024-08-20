from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from config.db import get_db
from .schemas import OrderRailWayRouteInDB, OrderRailWayRouteBase
from .services import OrderRailWayRouteService

router = APIRouter()


@router.get("/")
async def get_objs(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
    try:
        objs = await OrderRailWayRouteService.get_list(skip, limit, db)
        return objs
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to read order rail way: {str(e)}")


@router.get("/{obj_id}")
async def get_obj(obj_id: int, db: AsyncSession = Depends(get_db)):
    try:
        obj = await OrderRailWayRouteService.get_object(obj_id, db)
        if obj is None:
            raise HTTPException(status_code=404, detail="OrderRailWayRoute not found")
        return obj
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to read order rail way: {str(e)}")


@router.post("/", response_model=OrderRailWayRouteBase)
async def create_obj(obj: OrderRailWayRouteBase, db: AsyncSession = Depends(get_db)):
    try:
        new_obj = await OrderRailWayRouteService.create_object(obj, db)
        return OrderRailWayRouteInDB.from_orm(new_obj)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create order rail way: {str(e)}")


@router.delete("/{obj_id}")
async def delete_obj(obj_id: int, db: AsyncSession = Depends(get_db)):
    try:
        await OrderRailWayRouteService.delete_object(obj_id, db)
        return {"deleted": True}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete order rail way: {str(e)}")


@router.patch("/{obj_id}", response_model=OrderRailWayRouteBase)
async def update_bank_account(obj_id: int, obj_update: OrderRailWayRouteBase, db: AsyncSession = Depends(get_db)):
    try:
        obj = await OrderRailWayRouteService.update_object(obj_id, obj_update, db)
        if obj is None:
            raise HTTPException(status_code=404, detail="OrderRailWayRoute not found")
        return OrderRailWayRouteInDB.from_orm(obj)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update order rail way: {str(e)}")
