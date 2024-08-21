from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from config.db import get_db
from .data_rw import load_rw_json

router = APIRouter()


@router.post("/")
async def import_rail_way_dicts(db: AsyncSession = Depends(get_db)):
    try:
        rw = await load_rw_json(db)
        return {"status": "SUCCESS"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to import rail way dicts: {str(e)}")
