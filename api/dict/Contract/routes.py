from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from config.db import get_db
from .schemas import ContractInDB, ContractBase
from .services import ContractService

router = APIRouter()


@router.get("/")
async def get_objs(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
    try:
        objs = await ContractService.get_list(skip, limit, db)
        return objs
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to read contract: {str(e)}")


@router.get("/{obj_id}")
async def get_obj(obj_id: int, db: AsyncSession = Depends(get_db)):
    try:
        obj = await ContractService.get_object(obj_id, db)
        if obj is None:
            raise HTTPException(status_code=404, detail="Contract not found")
        return obj
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to read contract: {str(e)}")


@router.post("/", response_model=ContractBase)
async def create_obj(obj: ContractBase, db: AsyncSession = Depends(get_db)):
    try:
        new_obj = await ContractService.create_object(obj, db)
        return ContractInDB.from_orm(new_obj)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create contract: {str(e)}")


@router.delete("/{obj_id}")
async def delete_obj(obj_id: int, db: AsyncSession = Depends(get_db)):
    try:
        await ContractService.delete_object(obj_id, db)
        return {"deleted": True}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete contract: {str(e)}")


@router.patch("/{obj_id}", response_model=ContractBase)
async def update_contract(obj_id: int, obj_update: ContractBase, db: AsyncSession = Depends(get_db)):
    try:
        obj = await ContractService.update_object(obj_id, obj_update, db)
        if obj is None:
            raise HTTPException(status_code=404, detail="Contract not found")
        return ContractInDB.from_orm(obj)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update contract: {str(e)}")
