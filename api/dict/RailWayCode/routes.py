from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from config.db import get_db
from .schemas import RailWayCodeInDB, RailWayCodeBase
from .services import RailWayCodeService

router = APIRouter()


@router.get("/")
async def get_objs(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
    try:
        objs = await RailWayCodeService.get_list(skip, limit, db)
        return objs
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to read railway code: {str(e)}")


@router.get("/{obj_id}")
async def get_obj(obj_id: int, db: AsyncSession = Depends(get_db)):
    try:
        obj = await RailWayCodeService.get_object(obj_id, db)
        if obj is None:
            raise HTTPException(status_code=404, detail="RailWayCode not found")
        return obj
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to read railway code: {str(e)}")


@router.post("/", response_model=RailWayCodeBase)
async def create_obj(obj: RailWayCodeBase, db: AsyncSession = Depends(get_db)):
    try:
        new_obj = await RailWayCodeService.create_object(obj, db)
        return RailWayCodeInDB.from_orm(new_obj)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create railway code: {str(e)}")


@router.delete("/{obj_id}")
async def delete_obj(obj_id: int, db: AsyncSession = Depends(get_db)):
    try:
        await RailWayCodeService.delete_object(obj_id, db)
        return {"deleted": True}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete railway code: {str(e)}")


@router.patch("/{obj_id}", response_model=RailWayCodeBase)
async def update_organization(obj_id: int, obj_update: RailWayCodeBase, db: AsyncSession = Depends(get_db)):
    try:
        obj = await RailWayCodeService.update_object(obj_id, obj_update, db)
        if obj is None:
            raise HTTPException(status_code=404, detail="RailWayCode not found")
        return RailWayCodeInDB.from_orm(obj)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update railway code: {str(e)}")
