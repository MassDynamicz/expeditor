from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from api.dict.Station.schemas import StationRelate, StationCreate, StationUpdate, StationInDBBase
from api.dict.Territory.schemas import TerritoryInDBBase
from config.db import get_db
from api.dict.Station.models import Station
from typing import List


router = APIRouter()


# region РОУТ
@router.get("/", response_model=List[StationRelate])
async def read_stations(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(
            select(Station)
            .options(selectinload(Station.territory))
            .offset(skip).limit(limit)
        )
        stations = result.scalars().all()

        for station in stations:
            if station.territory:
                station.territory_data = TerritoryInDBBase.from_orm(station.territory)

        return [StationRelate.from_orm(station) for station in stations]
    except Exception as e:
        print(f"Ошибка чтения станции: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to read station: {str(e)}")


# станции по идентификатору
@router.get("/{station_id}", response_model=StationRelate)
async def read_station(station_id: int, db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(
            select(Station).options(selectinload(Station.territory)).where(Station.id == station_id)
        )
        station = result.scalars().one_or_none()
        if station is None:
            raise HTTPException(status_code=404, detail="Station not found")

        if station.territory:
            station.territory_data = TerritoryInDBBase.from_orm(station.territory)

        return StationRelate.from_orm(station)
    except Exception as e:
        print(f"Ошибка чтения станции: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to read station: {str(e)}")


# Создание новой станции или обновление существующей
@router.post("/", response_model=StationInDBBase)
async def create_or_update_station(station: StationCreate, db: AsyncSession = Depends(get_db)):
    try:
        # Создаем новую запись
        new_station = Station(**station.dict())
        db.add(new_station)
        await db.commit()
        await db.refresh(new_station)
        return StationInDBBase.from_orm(new_station)
    except Exception as e:
        print(f"Ошибка создания или обновления станции: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to create or update VAT: {str(e)}")


# Удаление станции по идентификатору
@router.delete("/{station_id}", response_model=StationInDBBase)
async def delete_station(station_id: int, db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(
            select(Station).where(Station.id == station_id)
        )
        station = result.scalars().one_or_none()
        if station is None:
            raise HTTPException(status_code=404, detail="Station not found")

        await db.delete(station)
        await db.commit()
        return StationInDBBase.from_orm(station)
    except Exception as e:
        print(f"Ошибка удаления станции: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to delete station: {str(e)}")


# Частичное обновление станции
@router.patch("/{station_id}", response_model=StationInDBBase)
async def update_station(station_id: int, station_update: StationUpdate, db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(
            select(Station).where(Station.id == station_id)
        )
        existing_station = result.scalars().one_or_none()

        if existing_station is None:
            raise HTTPException(status_code=404, detail="Station not found")

        for key, value in station_update.dict(exclude_unset=True).items():
            setattr(existing_station, key, value)

        await db.commit()
        await db.refresh(existing_station)
        return StationInDBBase.from_orm(existing_station)
    except Exception as e:
        print(f"Ошибка частичного обновления станции: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to update station: {str(e)}")
# endregion
