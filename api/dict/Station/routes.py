from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from config.db import get_db
from .schemas import StationInDB, StationBase
from .services import StationService

router = APIRouter()


@router.get("/")
async def get_objs(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
    try:
        objs = await StationService.get_list(skip, limit, db)
        return objs
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to read station: {str(e)}")


@router.get("/{obj_id}")
async def get_obj(obj_id: int, db: AsyncSession = Depends(get_db)):
    try:
        obj = await StationService.get_object(obj_id, db)
        if obj is None:
            raise HTTPException(status_code=404, detail="Station not found")
        return obj
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to read station: {str(e)}")


@router.post("/", response_model=StationBase)
async def create_obj(obj: StationBase, db: AsyncSession = Depends(get_db)):
    try:
        new_obj = await StationService.create_object(obj, db)
        return StationInDB.from_orm(new_obj)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create station: {str(e)}")


@router.delete("/{obj_id}")
async def delete_obj(obj_id: int, db: AsyncSession = Depends(get_db)):
    try:
        await StationService.delete_object(obj_id, db)
        return {"deleted": True}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete station: {str(e)}")


@router.patch("/{obj_id}", response_model=StationBase)
async def update_organization(obj_id: int, obj_update: StationBase, db: AsyncSession = Depends(get_db)):
    try:
        obj = await StationService.update_object(obj_id, obj_update, db)
        if obj is None:
            raise HTTPException(status_code=404, detail="Station not found")
        return StationInDB.from_orm(obj)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update station: {str(e)}")
