from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from config.db import get_db
from typing import List
from .schemas import CurrencyInDB, CurrencyBase
from .services import CurrencyService

router = APIRouter()


@router.get("/", response_model=List[CurrencyInDB])
async def get_objs(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
    try:
        objs = await CurrencyService.get_list(skip, limit, db)
        return [CurrencyInDB.from_orm(obj) for obj in objs]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to read currency: {str(e)}")


@router.get("/{obj_id}", response_model=CurrencyInDB)
async def get_obj(obj_id: int, db: AsyncSession = Depends(get_db)):
    try:
        obj = await CurrencyService.get_object(obj_id, db)
        if obj is None:
            raise HTTPException(status_code=404, detail="Currency not found")
        return CurrencyInDB.from_orm(obj)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to read currency: {str(e)}")


@router.post("/", response_model=CurrencyBase)
async def create_obj(obj: CurrencyBase, db: AsyncSession = Depends(get_db)):
    try:
        new_obj = await CurrencyService.create_object(obj, db)
        return CurrencyInDB.from_orm(new_obj)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create currency: {str(e)}")
