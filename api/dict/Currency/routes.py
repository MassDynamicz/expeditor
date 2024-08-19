from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from config.db import get_db
from .schemas import CurrencyInDB, CurrencyBase
from .services import CurrencyService

router = APIRouter()


@router.get("/")
async def get_objs(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
    try:
        objs = await CurrencyService.get_list(skip, limit, db)
        return objs
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to read currency: {str(e)}")


@router.get("/{obj_id}")
async def get_obj(obj_id: int, db: AsyncSession = Depends(get_db)):
    try:
        obj = await CurrencyService.get_object(obj_id, db)
        if obj is None:
            raise HTTPException(status_code=404, detail="Currency not found")
        return obj
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to read currency: {str(e)}")


@router.post("/", response_model=CurrencyBase)
async def create_obj(obj: CurrencyBase, db: AsyncSession = Depends(get_db)):
    try:
        new_obj = await CurrencyService.create_object(obj, db)
        return CurrencyInDB.from_orm(new_obj)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create currency: {str(e)}")


@router.delete("/{obj_id}")
async def delete_obj(obj_id: int, db: AsyncSession = Depends(get_db)):
    try:
        await CurrencyService.delete_object(obj_id, db)
        return {"deleted": True}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete currency: {str(e)}")


@router.patch("/{obj_id}", response_model=CurrencyBase)
async def update_currency(obj_id: int, obj_update: CurrencyBase, db: AsyncSession = Depends(get_db)):
    try:
        obj = await CurrencyService.update_object(obj_id, obj_update, db)
        if obj is None:
            raise HTTPException(status_code=404, detail="Currency not found")
        return CurrencyInDB.from_orm(obj)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update currency: {str(e)}")
