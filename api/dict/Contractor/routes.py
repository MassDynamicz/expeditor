from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from config.db import get_db
from .schemas import ContractorInDB, ContractorBase
from .services import ContractorService

router = APIRouter()


@router.get("/")
async def get_objs(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
    try:
        objs = await ContractorService.get_list(skip, limit, db)
        return objs
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to read contractor: {str(e)}")


@router.get("/{obj_id}")
async def get_obj(obj_id: int, db: AsyncSession = Depends(get_db)):
    try:
        obj = await ContractorService.get_object(obj_id, db)
        if obj is None:
            raise HTTPException(status_code=404, detail="Contractor not found")
        return obj
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to read contractor: {str(e)}")


@router.post("/", response_model=ContractorBase)
async def create_obj(obj: ContractorBase, db: AsyncSession = Depends(get_db)):
    try:
        new_obj = await ContractorService.create_object(obj, db)
        return ContractorInDB.from_orm(new_obj)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create contractor: {str(e)}")


@router.delete("/{obj_id}")
async def delete_obj(obj_id: int, db: AsyncSession = Depends(get_db)):
    try:
        await ContractorService.delete_object(obj_id, db)
        return {"deleted": True}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete contractor: {str(e)}")


@router.patch("/{obj_id}", response_model=ContractorBase)
async def update_contractor(obj_id: int, obj_update: ContractorBase, db: AsyncSession = Depends(get_db)):
    try:
        obj = await ContractorService.update_object(obj_id, obj_update, db)
        if obj is None:
            raise HTTPException(status_code=404, detail="Contractor not found")
        return ContractorInDB.from_orm(obj)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update contractor: {str(e)}")
