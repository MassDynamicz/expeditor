from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from config.db import get_db
from typing import List
from .schemas import CountryInDB, CountryBase
from .services import CountryService

router = APIRouter()


@router.get("/", response_model=List[CountryInDB])
async def get_objs(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
    try:
        objs = await CountryService.get_list(skip, limit, db)
        return [CountryInDB.from_orm(obj) for obj in objs]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to read countries: {str(e)}")


@router.get("/{obj_id}", response_model=CountryInDB)
async def get_obj(obj_id: int, db: AsyncSession = Depends(get_db)):
    try:
        obj = await CountryService.get_object(obj_id, db)
        if obj is None:
            raise HTTPException(status_code=404, detail="Country not found")
        return CountryInDB.from_orm(obj)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to read country: {str(e)}")


@router.post("/", response_model=CountryBase)
async def create_obj(obj: CountryBase, db: AsyncSession = Depends(get_db)):
    try:
        new_obj = await CountryService.create_object(obj, db)
        return CountryInDB.from_orm(new_obj)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create country: {str(e)}")
