from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from config.db import get_db
from api.dict.Country.models import Country
from api.dict.Country.schemas import CountryInDBBase, CountryCreate, CountryUpdate
from typing import List

router = APIRouter()


# Список стран
@router.get("/", response_model=List[CountryInDBBase])
async def read_countries(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(
            select(Country)
            .offset(skip).limit(limit)
        )
        countries = result.scalars().all()
        return [CountryInDBBase.from_orm(country) for country in countries]
    except Exception as e:
        print(f"Ошибка чтения стран: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to read countries: {str(e)}")


# Страна по идентификатору
@router.get("/{country_id}", response_model=CountryInDBBase)
async def read_country(country_id: int, db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(
            select(Country).where(Country.id == country_id)
        )
        country = result.scalars().one_or_none()
        if country is None:
            raise HTTPException(status_code=404, detail="Country not found")
        return CountryInDBBase.from_orm(country)
    except Exception as e:
        print(f"Ошибка чтения страны: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to read country: {str(e)}")


# Создание новой страны или обновление существующей
@router.post("/", response_model=CountryInDBBase)
async def create_or_update_country(country: CountryCreate, db: AsyncSession = Depends(get_db)):
    try:
        if country.guid == "":
            # Создаем новую запись
            new_country = Country(**country.dict())
            db.add(new_country)
            await db.commit()
            await db.refresh(new_country)
            return CountryInDBBase.from_orm(new_country)

        result = await db.execute(
            select(Country).where(Country.guid == country.guid)
        )
        existing_country = result.scalars().one_or_none()

        if existing_country:
            # Обновляем существующую запись
            for key, value in country.dict().items():
                setattr(existing_country, key, value)
            await db.commit()
            await db.refresh(existing_country)
            return CountryInDBBase.from_orm(existing_country)
        else:
            # Создаем новую запись
            new_country = Country(**country.dict())
            db.add(new_country)
            await db.commit()
            await db.refresh(new_country)
            return CountryInDBBase.from_orm(new_country)
    except Exception as e:
        print(f"Ошибка создания или обновления страны: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to create or update country: {str(e)}")


# Удаление страны по идентификатору
@router.delete("/{country_id}", response_model=CountryInDBBase)
async def delete_country(country_id: int, db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(
            select(Country).where(Country.id == country_id)
        )
        country = result.scalars().one_or_none()
        if country is None:
            raise HTTPException(status_code=404, detail="Country not found")

        await db.delete(country)
        await db.commit()
        return CountryInDBBase.from_orm(country)
    except Exception as e:
        print(f"Ошибка удаления страны: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to delete country: {str(e)}")


# Частичное обновление страны
@router.patch("/{country_id}", response_model=CountryInDBBase)
async def update_country(country_id: int, country_update: CountryUpdate, db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(
            select(Country).where(Country.id == country_id)
        )
        existing_country = result.scalars().one_or_none()

        if existing_country is None:
            raise HTTPException(status_code=404, detail="Country not found")

        for key, value in country_update.dict(exclude_unset=True).items():
            setattr(existing_country, key, value)

        await db.commit()
        await db.refresh(existing_country)
        return CountryInDBBase.from_orm(existing_country)
    except Exception as e:
        print(f"Ошибка частичного обновления страны: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to update country: {str(e)}")
