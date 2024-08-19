from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from config.db import get_db
from .schemas import TerritoryInDB, TerritoryBase
from .services import TerritoryService

router = APIRouter()


@router.get("/")
async def get_objs(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
    try:
        objs = await TerritoryService.get_list(skip, limit, db)
        return objs
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to read territory: {str(e)}")


@router.get("/{obj_id}")
async def get_obj(obj_id: int, db: AsyncSession = Depends(get_db)):
    try:
        obj = await TerritoryService.get_object(obj_id, db)
        if obj is None:
            raise HTTPException(status_code=404, detail="Territory not found")
        return obj
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to read territory: {str(e)}")


@router.post("/", response_model=TerritoryBase)
async def create_obj(obj: TerritoryBase, db: AsyncSession = Depends(get_db)):
    try:
        new_obj = await TerritoryService.create_object(obj, db)
        return TerritoryInDB.from_orm(new_obj)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create territory: {str(e)}")


@router.delete("/{obj_id}")
async def delete_obj(obj_id: int, db: AsyncSession = Depends(get_db)):
    try:
        await TerritoryService.delete_object(obj_id, db)
        return {"deleted": True}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete territory: {str(e)}")


@router.patch("/{obj_id}", response_model=TerritoryBase)
async def update_vat(obj_id: int, obj_update: TerritoryBase, db: AsyncSession = Depends(get_db)):
    try:
        obj = await TerritoryService.update_object(obj_id, obj_update, db)
        if obj is None:
            raise HTTPException(status_code=404, detail="Territory not found")
        return TerritoryInDB.from_orm(obj)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update territory: {str(e)}")
