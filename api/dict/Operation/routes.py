from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from config.db import get_db
from .schemas import OperationInDB, OperationBase
from .services import OperationService

router = APIRouter()


@router.get("/")
async def get_objs(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
    try:
        objs = await OperationService.get_list(skip, limit, db)
        return objs
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to read operation: {str(e)}")


@router.get("/{obj_id}")
async def get_obj(obj_id: int, db: AsyncSession = Depends(get_db)):
    try:
        obj = await OperationService.get_object(obj_id, db)
        if obj is None:
            raise HTTPException(status_code=404, detail="Operation not found")
        return obj
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to read operation: {str(e)}")


@router.post("/", response_model=OperationBase)
async def create_obj(obj: OperationBase, db: AsyncSession = Depends(get_db)):
    try:
        new_obj = await OperationService.create_object(obj, db)
        return OperationInDB.from_orm(new_obj)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create operation: {str(e)}")


@router.delete("/{obj_id}")
async def delete_obj(obj_id: int, db: AsyncSession = Depends(get_db)):
    try:
        await OperationService.delete_object(obj_id, db)
        return {"deleted": True}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete operation: {str(e)}")


@router.patch("/{obj_id}", response_model=OperationBase)
async def update_organization(obj_id: int, obj_update: OperationBase, db: AsyncSession = Depends(get_db)):
    try:
        obj = await OperationService.update_object(obj_id, obj_update, db)
        if obj is None:
            raise HTTPException(status_code=404, detail="Operation not found")
        return OperationInDB.from_orm(obj)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update operation: {str(e)}")
