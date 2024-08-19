from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from config.db import get_db
from .schemas import GngInDB, GngBase
from .services import GngService

router = APIRouter()


@router.get("/")
async def get_objs(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
    try:
        objs = await GngService.get_list(skip, limit, db)
        return objs
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to read gng: {str(e)}")


@router.get("/{obj_id}")
async def get_obj(obj_id: int, db: AsyncSession = Depends(get_db)):
    try:
        obj = await GngService.get_object(obj_id, db)
        if obj is None:
            raise HTTPException(status_code=404, detail="Gng not found")
        return obj
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to read gng: {str(e)}")


@router.post("/", response_model=GngBase)
async def create_obj(obj: GngBase, db: AsyncSession = Depends(get_db)):
    try:
        new_obj = await GngService.create_object(obj, db)
        return GngInDB.from_orm(new_obj)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create gng: {str(e)}")


@router.delete("/{obj_id}")
async def delete_obj(obj_id: int, db: AsyncSession = Depends(get_db)):
    try:
        await GngService.delete_object(obj_id, db)
        return {"deleted": True}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete gng: {str(e)}")


@router.patch("/{obj_id}", response_model=GngBase)
async def update_vat(obj_id: int, obj_update: GngBase, db: AsyncSession = Depends(get_db)):
    try:
        obj = await GngService.update_object(obj_id, obj_update, db)
        if obj is None:
            raise HTTPException(status_code=404, detail="Gng not found")
        return GngInDB.from_orm(obj)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update etsn: {str(e)}")
