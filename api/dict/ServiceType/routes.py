from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from config.db import get_db
from .schemas import ServiceTypeInDB, ServiceTypeBase
from .services import ServiceTypeService

router = APIRouter()


@router.get("/")
async def get_objs(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
    try:
        objs = await ServiceTypeService.get_list(skip, limit, db)
        return objs
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to read service type: {str(e)}")


@router.get("/{obj_id}")
async def get_obj(obj_id: int, db: AsyncSession = Depends(get_db)):
    try:
        obj = await ServiceTypeService.get_object(obj_id, db)
        if obj is None:
            raise HTTPException(status_code=404, detail="ServiceType not found")
        return obj
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to read service type: {str(e)}")


@router.post("/", response_model=ServiceTypeBase)
async def create_obj(obj: ServiceTypeBase, db: AsyncSession = Depends(get_db)):
    try:
        new_obj = await ServiceTypeService.create_object(obj, db)
        return ServiceTypeInDB.from_orm(new_obj)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create service type: {str(e)}")


@router.delete("/{obj_id}")
async def delete_obj(obj_id: int, db: AsyncSession = Depends(get_db)):
    try:
        await ServiceTypeService.delete_object(obj_id, db)
        return {"deleted": True}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete service type: {str(e)}")


@router.patch("/{obj_id}", response_model=ServiceTypeBase)
async def update_vat(obj_id: int, obj_update: ServiceTypeBase, db: AsyncSession = Depends(get_db)):
    try:
        obj = await ServiceTypeService.update_object(obj_id, obj_update, db)
        if obj is None:
            raise HTTPException(status_code=404, detail="ServiceType not found")
        return ServiceTypeInDB.from_orm(obj)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update service type: {str(e)}")
