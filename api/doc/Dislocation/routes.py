from sqlalchemy import select
from config.db import get_db
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from .models import Dislocation
from .schemas import DislocationBase

router = APIRouter()

@router.get("/", response_model=List[DislocationBase])
async def read_dislocation(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
    async with db as session:
        result = await session.execute(
            select(Dislocation).offset(skip).limit(limit)
        )
        dislocations = result.scalars().all()
        return dislocations
