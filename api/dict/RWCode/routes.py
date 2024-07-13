from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from api.dict.RWCode.schemas import RWCodeInDBBase, RWCodeUpdate, RWCodeCreate
from config.db import get_db
from api.dict.RWCode.models import RWCode
from typing import List


router = APIRouter()


@router.get("/", response_model=List[RWCodeInDBBase])
async def read_obj(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(select(RWCode).offset(skip).limit(limit))
        rwcode = result.scalars().all()
        return [RWCodeInDBBase.from_orm(rwcode) for rwcode in rwcode]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to read rw codes: {str(e)}")


@router.get("/{obj_id}", response_model=RWCodeInDBBase)
async def read_obj(obj_id: int, db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(select(RWCode).where(RWCode.id == obj_id))
        obj = result.scalars().one_or_none()
        if obj is None:
            raise HTTPException(status_code=404, detail="RW code not found")
        return RWCodeInDBBase.from_orm(obj)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to read rw code: {str(e)}")


@router.post("/", response_model=RWCodeCreate)
async def create_or_update_obj(rw_code: RWCodeCreate, db: AsyncSession = Depends(get_db)):
    try:
        new_rwcode = RWCode(**rw_code.dict())
        db.add(new_rwcode)
        await db.commit()
        await db.refresh(new_rwcode)
        return RWCodeCreate.from_orm(new_rwcode)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create or update rw code: {str(e)}")


@router.delete("/{obj_id}", response_model=RWCodeInDBBase)
async def delete_rw_code(obj_id: int, db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(select(RWCode).where(RWCode.id == obj_id))
        obj = result.scalars().one_or_none()
        if obj is None:
            raise HTTPException(status_code=404, detail="RW code not found")
        await db.delete(obj)
        await db.commit()
        return RWCodeInDBBase.from_orm(obj)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete rw_code: {str(e)}")


@router.patch("/{obj_id}", response_model=RWCodeUpdate)
async def update_rw_code(obj_id: int, rwcode_update: RWCodeUpdate, db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(select(RWCode).where(RWCode.id == obj_id))
        existing_rwcode = result.scalars().one_or_none()
        if existing_rwcode is None:
            raise HTTPException(status_code=404, detail="RW code not found")
        for key, value in rwcode_update.dict(exclude_unset=True).items():
            setattr(existing_rwcode, key, value)
        await db.commit()
        await db.refresh(existing_rwcode)
        return RWCodeUpdate.from_orm(existing_rwcode)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update rw code: {str(e)}")
# endregion
