from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from api.dict.Subcode.schemas import SubcodeInDBBase, SubcodeUpdate, SubcodeCreate
from config.db import get_db
from api.dict.Subcode.models import Subcode
from typing import List


router = APIRouter()


@router.get("/", response_model=List[SubcodeInDBBase])
async def read_obj(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(select(Subcode).offset(skip).limit(limit))
        subcode = result.scalars().all()
        return [SubcodeInDBBase.from_orm(subcode) for subcode in subcode]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to read subcodes: {str(e)}")


@router.get("/{obj_id}", response_model=SubcodeInDBBase)
async def read_obj(obj_id: int, db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(select(Subcode).where(Subcode.id == obj_id))
        obj = result.scalars().one_or_none()
        if obj is None:
            raise HTTPException(status_code=404, detail="Subcode not found")
        return SubcodeInDBBase.from_orm(obj)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to read subcode: {str(e)}")


@router.post("/", response_model=SubcodeCreate)
async def create_or_update_obj(rw_code: SubcodeCreate, db: AsyncSession = Depends(get_db)):
    try:
        new_subcode = Subcode(**rw_code.dict())
        db.add(new_subcode)
        await db.commit()
        await db.refresh(new_subcode)
        return SubcodeCreate.from_orm(new_subcode)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create or update subcode: {str(e)}")


@router.delete("/{obj_id}", response_model=SubcodeInDBBase)
async def delete_subcode(obj_id: int, db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(select(Subcode).where(Subcode.id == obj_id))
        obj = result.scalars().one_or_none()
        if obj is None:
            raise HTTPException(status_code=404, detail="Subcode not found")
        await db.delete(obj)
        await db.commit()
        return SubcodeInDBBase.from_orm(obj)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete subcode: {str(e)}")


@router.patch("/{obj_id}", response_model=SubcodeUpdate)
async def update_subcode(obj_id: int, subcode_update: SubcodeUpdate, db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(select(Subcode).where(Subcode.id == obj_id))
        existing_subcode = result.scalars().one_or_none()
        if existing_subcode is None:
            raise HTTPException(status_code=404, detail="Subcode not found")
        for key, value in subcode_update.dict(exclude_unset=True).items():
            setattr(existing_subcode, key, value)
        await db.commit()
        await db.refresh(existing_subcode)
        return SubcodeUpdate.from_orm(existing_subcode)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update subcode: {str(e)}")
# endregion
