from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from config.db import get_db
from typing import List
from .schemas import ContractorInDB, ContractorBase
from .services import ContractorService

router = APIRouter()


@router.get("/", response_model=List[ContractorInDB])
async def get_objs(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
    try:
        objs = await ContractorService.get_list(skip, limit, db)
        return [ContractorInDB.from_orm(obj) for obj in objs]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to read contractor: {str(e)}")


@router.get("/{obj_id}", response_model=ContractorInDB)
async def get_obj(obj_id: int, db: AsyncSession = Depends(get_db)):
    try:
        obj = await ContractorService.get_object(obj_id, db)
        if obj is None:
            raise HTTPException(status_code=404, detail="Contractor not found")
        return ContractorInDB.from_orm(obj)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to read contractor: {str(e)}")


@router.post("/", response_model=ContractorBase)
async def create_obj(obj: ContractorBase, db: AsyncSession = Depends(get_db)):
    try:
        new_obj = await ContractorService.create_object(obj, db)
        return ContractorInDB.from_orm(new_obj)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create contractor: {str(e)}")
