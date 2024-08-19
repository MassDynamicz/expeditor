from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from config.db import get_db
from .schemas import WagonInDB, WagonBase
from .services import WagonService

router = APIRouter()


@router.get("/")
async def get_objs(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
    try:
        objs = await WagonService.get_list(skip, limit, db)
        return objs
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to read wagon: {str(e)}")


@router.get("/{obj_id}")
async def get_obj(obj_id: int, db: AsyncSession = Depends(get_db)):
    try:
        obj = await WagonService.get_object(obj_id, db)
        if obj is None:
            raise HTTPException(status_code=404, detail="Wagon not found")
        return obj
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to read wagon: {str(e)}")


@router.post("/", response_model=WagonBase)
async def create_obj(obj: WagonBase, db: AsyncSession = Depends(get_db)):
    try:
        new_obj = await WagonService.create_object(obj, db)
        return WagonInDB.from_orm(new_obj)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create wagon: {str(e)}")


@router.delete("/{obj_id}")
async def delete_obj(obj_id: int, db: AsyncSession = Depends(get_db)):
    try:
        await WagonService.delete_object(obj_id, db)
        return {"deleted": True}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete wagon: {str(e)}")


@router.patch("/{obj_id}", response_model=WagonBase)
async def update_organization(obj_id: int, obj_update: WagonBase, db: AsyncSession = Depends(get_db)):
    try:
        obj = await WagonService.update_object(obj_id, obj_update, db)
        if obj is None:
            raise HTTPException(status_code=404, detail="Wagon not found")
        return WagonInDB.from_orm(obj)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update wagon: {str(e)}")
