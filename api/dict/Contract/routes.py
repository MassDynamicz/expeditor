from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from config.db import get_db
from typing import List
from .schemas import ContractInDB, ContractBase
from .services import ContractService

router = APIRouter()


@router.get("/", response_model=List[ContractInDB])
async def get_objs(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
    try:
        objs = await ContractService.get_list(skip, limit, db)
        return [ContractInDB.from_orm(obj) for obj in objs]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to read Contract: {str(e)}")


@router.get("/{obj_id}", response_model=ContractInDB)
async def get_obj(obj_id: int, db: AsyncSession = Depends(get_db)):
    try:
        obj = await ContractService.get_object(obj_id, db)
        if obj is None:
            raise HTTPException(status_code=404, detail="Contract not found")
        return ContractInDB.from_orm(obj)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to read Contract: {str(e)}")


@router.post("/", response_model=ContractBase)
async def create_obj(obj: ContractBase, db: AsyncSession = Depends(get_db)):
    try:
        new_obj = await ContractService.create_object(obj, db)
        return ContractInDB.from_orm(new_obj)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create Contract: {str(e)}")
