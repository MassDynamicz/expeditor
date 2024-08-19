from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from config.db import get_db
from .schemas import WagonTypeInDB, WagonTypeBase
from .services import WagonTypeService

router = APIRouter()


@router.get("/")
async def get_objs(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
    try:
        objs = await WagonTypeService.get_list(skip, limit, db)
        return objs
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to read wagon type: {str(e)}")


@router.get("/{obj_id}")
async def get_obj(obj_id: int, db: AsyncSession = Depends(get_db)):
    try:
        obj = await WagonTypeService.get_object(obj_id, db)
        if obj is None:
            raise HTTPException(status_code=404, detail="WagonType not found")
        return obj
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to read wagon type: {str(e)}")


@router.post("/", response_model=WagonTypeBase)
async def create_obj(obj: WagonTypeBase, db: AsyncSession = Depends(get_db)):
    try:
        new_obj = await WagonTypeService.create_object(obj, db)
        return WagonTypeInDB.from_orm(new_obj)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create wagon type: {str(e)}")


@router.delete("/{obj_id}")
async def delete_obj(obj_id: int, db: AsyncSession = Depends(get_db)):
    try:
        await WagonTypeService.delete_object(obj_id, db)
        return {"deleted": True}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete wagon type: {str(e)}")


@router.patch("/{obj_id}", response_model=WagonTypeBase)
async def update_vat(obj_id: int, obj_update: WagonTypeBase, db: AsyncSession = Depends(get_db)):
    try:
        obj = await WagonTypeService.update_object(obj_id, obj_update, db)
        if obj is None:
            raise HTTPException(status_code=404, detail="WagonType not found")
        return WagonTypeInDB.from_orm(obj)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update wagon type: {str(e)}")
