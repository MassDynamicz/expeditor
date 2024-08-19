from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from config.db import get_db
from .schemas import ContainerInDB, ContainerBase
from .services import ContainerService

router = APIRouter()


@router.get("/")
async def get_objs(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
    try:
        objs = await ContainerService.get_list(skip, limit, db)
        return objs
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to read container: {str(e)}")


@router.get("/{obj_id}")
async def get_obj(obj_id: int, db: AsyncSession = Depends(get_db)):
    try:
        obj = await ContainerService.get_object(obj_id, db)
        if obj is None:
            raise HTTPException(status_code=404, detail="Container not found")
        return obj
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to read container: {str(e)}")


@router.post("/", response_model=ContainerBase)
async def create_obj(obj: ContainerBase, db: AsyncSession = Depends(get_db)):
    try:
        new_obj = await ContainerService.create_object(obj, db)
        return ContainerInDB.from_orm(new_obj)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create container: {str(e)}")


@router.delete("/{obj_id}")
async def delete_obj(obj_id: int, db: AsyncSession = Depends(get_db)):
    try:
        await ContainerService.delete_object(obj_id, db)
        return {"deleted": True}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete container: {str(e)}")


@router.patch("/{obj_id}", response_model=ContainerBase)
async def update_organization(obj_id: int, obj_update: ContainerBase, db: AsyncSession = Depends(get_db)):
    try:
        obj = await ContainerService.update_object(obj_id, obj_update, db)
        if obj is None:
            raise HTTPException(status_code=404, detail="Container not found")
        return ContainerInDB.from_orm(obj)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update container: {str(e)}")
