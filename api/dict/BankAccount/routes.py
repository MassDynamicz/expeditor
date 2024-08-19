from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from config.db import get_db
from .schemas import BankAccountInDB, BankAccountBase
from .services import BankAccountService

router = APIRouter()


@router.get("/")
async def get_objs(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
    try:
        objs = await BankAccountService.get_list(skip, limit, db)
        return objs
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to read bank_account: {str(e)}")


@router.get("/{obj_id}")
async def get_obj(obj_id: int, db: AsyncSession = Depends(get_db)):
    try:
        obj = await BankAccountService.get_object(obj_id, db)
        if obj is None:
            raise HTTPException(status_code=404, detail="BankAccount not found")
        return obj
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to read bank_account: {str(e)}")


@router.post("/", response_model=BankAccountBase)
async def create_obj(obj: BankAccountBase, db: AsyncSession = Depends(get_db)):
    try:
        new_obj = await BankAccountService.create_object(obj, db)
        return BankAccountInDB.from_orm(new_obj)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create bank_account: {str(e)}")


@router.delete("/{obj_id}")
async def delete_obj(obj_id: int, db: AsyncSession = Depends(get_db)):
    try:
        await BankAccountService.delete_object(obj_id, db)
        return {"deleted": True}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete bank_account: {str(e)}")


@router.patch("/{obj_id}", response_model=BankAccountBase)
async def update_bank_account(obj_id: int, obj_update: BankAccountBase, db: AsyncSession = Depends(get_db)):
    try:
        obj = await BankAccountService.update_object(obj_id, obj_update, db)
        if obj is None:
            raise HTTPException(status_code=404, detail="BankAccount not found")
        return BankAccountInDB.from_orm(obj)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update bank_account: {str(e)}")
