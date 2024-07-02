from fastapi import Request
import json
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from api.dict.Currency.models import Currency
from api.dict.Country.models import Country


async def receive_json_1c(request: Request, session: AsyncSession):
    try:
        data = await request.json()
        # Обработка полученного JSON
        await parse_json_data(session, data)
        return {"message": "JSON received successfully", "status": "OK"}
    except json.JSONDecodeError:
        return {"error": "Invalid JSON", "status": "ERROR"}


async def parse_json_data(session: AsyncSession, data: dict):
    # Загружаем валюты из 1С
    for currency_data in data.get('Currency', []):
        guid = currency_data['guid']
        result = await session.execute(select(Currency).filter_by(guid=guid))
        existing_currency = result.scalar_one_or_none()
        if existing_currency:
            # Обновляем существующий объект
            for key, value in currency_data.items():
                setattr(existing_currency, key, value)
        else:
            # Создаем новый объект
            new_currency = Currency(**currency_data)
            session.add(new_currency)

    # Загружаем страны из 1С
    for counttry_data in data.get('Country', []):
        guid = counttry_data['guid']
        name = counttry_data['name']
        full_name = counttry_data['full_name']
        code = counttry_data['code']

        # Проверка существования объекта по guid
        result = await session.execute(select(Country).filter(Country.guid == guid))
        country = result.scalars().first()

        if country:
            # Если объект существует, обновляем его
            country.name = name
            country.full_name = full_name
            country.code = code
        else:
            # Если объект не существует, создаем новый
            new_country = Country(
                guid=guid,
                name=name,
                full_name=full_name,
                code=code
            )
            session.add(new_country)

    await session.commit()
