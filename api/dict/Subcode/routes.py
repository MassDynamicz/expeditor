from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from config.db import get_db
from .schemas import SubcodeInDB, SubcodeBase
from .services import SubcodeService

router = APIRouter()


@router.get("/")
async def get_objs(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
    try:
        objs = await SubcodeService.get_list(skip, limit, db)
        return objs
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to read subcode: {str(e)}")


@router.get("/{obj_id}")
async def get_obj(obj_id: int, db: AsyncSession = Depends(get_db)):
    try:
        obj = await SubcodeService.get_object(obj_id, db)
        if obj is None:
            raise HTTPException(status_code=404, detail="Subcode not found")
        return obj
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to read subcode: {str(e)}")


@router.post("/", response_model=SubcodeBase)
async def create_obj(obj: SubcodeBase, db: AsyncSession = Depends(get_db)):
    try:
        new_obj = await SubcodeService.create_object(obj, db)
        return SubcodeInDB.from_orm(new_obj)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create subcode: {str(e)}")


@router.delete("/{obj_id}")
async def delete_obj(obj_id: int, db: AsyncSession = Depends(get_db)):
    try:
        await SubcodeService.delete_object(obj_id, db)
        return {"deleted": True}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete subcode: {str(e)}")


@router.patch("/{obj_id}", response_model=SubcodeBase)
async def update_organization(obj_id: int, obj_update: SubcodeBase, db: AsyncSession = Depends(get_db)):
    try:
        obj = await SubcodeService.update_object(obj_id, obj_update, db)
        if obj is None:
            raise HTTPException(status_code=404, detail="Subcode not found")
        return SubcodeInDB.from_orm(obj)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update subcode: {str(e)}")
