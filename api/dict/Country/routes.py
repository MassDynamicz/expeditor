from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from config.db import get_db
from .schemas import CountryInDB, CountryBase
from .services import CountryService

router = APIRouter()


@router.get("/")
async def get_objs(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
    try:
        objs = await CountryService.get_list(skip, limit, db)
        return objs
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to read country: {str(e)}")


@router.get("/{obj_id}")
async def get_obj(obj_id: int, db: AsyncSession = Depends(get_db)):
    try:
        obj = await CountryService.get_object(obj_id, db)
        if obj is None:
            raise HTTPException(status_code=404, detail="Country not found")
        return obj
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to read country: {str(e)}")


@router.post("/", response_model=CountryBase)
async def create_obj(obj: CountryBase, db: AsyncSession = Depends(get_db)):
    try:
        new_obj = await CountryService.create_object(obj, db)
        return CountryInDB.from_orm(new_obj)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create country: {str(e)}")


@router.delete("/{obj_id}")
async def delete_obj(obj_id: int, db: AsyncSession = Depends(get_db)):
    try:
        await CountryService.delete_object(obj_id, db)
        return {"deleted": True}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete country: {str(e)}")


@router.patch("/{obj_id}", response_model=CountryBase)
async def update_country(obj_id: int, obj_update: CountryBase, db: AsyncSession = Depends(get_db)):
    try:
        obj = await CountryService.update_object(obj_id, obj_update, db)
        if obj is None:
            raise HTTPException(status_code=404, detail="Country not found")
        return CountryInDB.from_orm(obj)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update country: {str(e)}")
