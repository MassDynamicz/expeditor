from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from config.db import get_db
from typing import List
from .schemas import BankInDB, BankBase
from .services import BankService

router = APIRouter()


@router.get("/", response_model=List[BankInDB])
async def get_objs(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
    try:
        objs = await BankService.get_list(skip, limit, db)
        return [BankInDB.from_orm(obj) for obj in objs]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to read bank: {str(e)}")


@router.get("/{obj_id}", response_model=BankInDB)
async def get_obj(obj_id: int, db: AsyncSession = Depends(get_db)):
    try:
        obj = await BankService.get_object(obj_id, db)
        if obj is None:
            raise HTTPException(status_code=404, detail="Bank not found")
        return BankInDB.from_orm(obj)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to read bank: {str(e)}")


@router.post("/", response_model=BankBase)
async def create_obj(obj: BankBase, db: AsyncSession = Depends(get_db)):
    try:
        new_obj = await BankService.create_object(obj, db)
        return BankInDB.from_orm(new_obj)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create bank: {str(e)}")


@router.delete("/{obj_id}")
async def delete_obj(obj_id: int, db: AsyncSession = Depends(get_db)):
    try:
        await BankService.delete_object(obj_id, db)
        return {"deleted": True}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete bank: {str(e)}")


@router.patch("/{obj_id}", response_model=BankBase)
async def update_bank(obj_id: int, obj_update: BankBase, db: AsyncSession = Depends(get_db)):
    try:
        obj = await BankService.update_object(obj_id, obj_update, db)
        if obj is None:
            raise HTTPException(status_code=404, detail="Bank not found")
        return BankInDB.from_orm(obj)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update bank: {str(e)}")
