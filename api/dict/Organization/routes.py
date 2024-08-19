from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from config.db import get_db
from .schemas import OrganizationInDB, OrganizationBase
from .services import OrganizationService

router = APIRouter()


@router.get("/")
async def get_objs(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
    try:
        objs = await OrganizationService.get_list(skip, limit, db)
        return objs
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to read organization: {str(e)}")


@router.get("/{obj_id}")
async def get_obj(obj_id: int, db: AsyncSession = Depends(get_db)):
    try:
        obj = await OrganizationService.get_object(obj_id, db)
        if obj is None:
            raise HTTPException(status_code=404, detail="Organization not found")
        return obj
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to read organization: {str(e)}")


@router.post("/", response_model=OrganizationBase)
async def create_obj(obj: OrganizationBase, db: AsyncSession = Depends(get_db)):
    try:
        new_obj = await OrganizationService.create_object(obj, db)
        return OrganizationInDB.from_orm(new_obj)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create organization: {str(e)}")


@router.delete("/{obj_id}")
async def delete_obj(obj_id: int, db: AsyncSession = Depends(get_db)):
    try:
        await OrganizationService.delete_object(obj_id, db)
        return {"deleted": True}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete organization: {str(e)}")


@router.patch("/{obj_id}", response_model=OrganizationBase)
async def update_organization(obj_id: int, obj_update: OrganizationBase, db: AsyncSession = Depends(get_db)):
    try:
        obj = await OrganizationService.update_object(obj_id, obj_update, db)
        if obj is None:
            raise HTTPException(status_code=404, detail="Organization not found")
        return OrganizationInDB.from_orm(obj)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update organization: {str(e)}")
