from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from config.db import get_db
from .schemas import VatInDB, VatBase
from .services import VatService

router = APIRouter()


@router.get("/")
async def get_objs(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
    try:
        objs = await VatService.get_list(skip, limit, db)
        return objs
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to read vat: {str(e)}")


@router.get("/{obj_id}")
async def get_obj(obj_id: int, db: AsyncSession = Depends(get_db)):
    try:
        obj = await VatService.get_object(obj_id, db)
        if obj is None:
            raise HTTPException(status_code=404, detail="Vat not found")
        return obj
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to read vat: {str(e)}")


@router.post("/", response_model=VatBase)
async def create_obj(obj: VatBase, db: AsyncSession = Depends(get_db)):
    try:
        new_obj = await VatService.create_object(obj, db)
        return VatInDB.from_orm(new_obj)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create vat: {str(e)}")


@router.delete("/{obj_id}")
async def delete_obj(obj_id: int, db: AsyncSession = Depends(get_db)):
    try:
        await VatService.delete_object(obj_id, db)
        return {"deleted": True}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete vat: {str(e)}")


@router.patch("/{obj_id}", response_model=VatBase)
async def update_vat(obj_id: int, obj_update: VatBase, db: AsyncSession = Depends(get_db)):
    try:
        obj = await VatService.update_object(obj_id, obj_update, db)
        if obj is None:
            raise HTTPException(status_code=404, detail="Vat not found")
        return VatInDB.from_orm(obj)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update vat: {str(e)}")
