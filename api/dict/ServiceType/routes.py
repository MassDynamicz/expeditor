from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from config.db import get_db
from typing import List
from .schemas import ServiceTypeInDB, ServiceTypeBase
from .services import ServiceTypeService

router = APIRouter()


@router.get("/", response_model=List[ServiceTypeInDB])
async def get_objs(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
    try:
        objs = await ServiceTypeService.get_list(skip, limit, db)
        return [ServiceTypeInDB.from_orm(obj) for obj in objs]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to read service type: {str(e)}")


@router.get("/{obj_id}", response_model=ServiceTypeInDB)
async def get_obj(obj_id: int, db: AsyncSession = Depends(get_db)):
    try:
        obj = await ServiceTypeService.get_object(obj_id, db)
        if obj is None:
            raise HTTPException(status_code=404, detail="ServiceType not found")
        return ServiceTypeInDB.from_orm(obj)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to read service type: {str(e)}")


@router.post("/", response_model=ServiceTypeBase)
async def create_obj(obj: ServiceTypeBase, db: AsyncSession = Depends(get_db)):
    try:
        new_obj = await ServiceTypeService.create_object(obj, db)
        return ServiceTypeInDB.from_orm(new_obj)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create service type: {str(e)}")
