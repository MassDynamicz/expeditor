from fastapi import Request
import json
from sqlalchemy.ext.asyncio import AsyncSession
import os
from sqlalchemy.future import select

from api.dict.Etsng.models import Etsng
from api.dict.Gng.models import Gng
from api.dict.Station.models import Station
from api.dict.Territory.models import Territory
from api.dict.WagonType.models import WagonType


async def load_rw_json(request: Request, session: AsyncSession):
    try:
        await load_territories(session)
        await load_stations(session)
        await load_wagon_types(session)
        await load_etsn(session)
        await load_gng(session)

        return {"status": "SUCCESS"}
    except json.JSONDecodeError:
        return {"error": "Invalid JSON", "status": "ERROR"}


# Загружаем территории ЖД
async def load_territories(session):
    current_dir = os.path.dirname(__file__)
    json_file = os.path.join(current_dir, 'territories.json')

    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Обработка полученного JSON
    for territory in data:
        name = territory['name']
        code = territory['code']

        result = await session.execute(select(Territory).filter(Territory.code == code))
        obj = result.scalars().first()
        if not obj:
            new_territory = Territory(
                code=code,
                name=name
            )
            session.add(new_territory)
    await session.commit()


# Загружаем территории ЖД
async def load_stations(session):
    current_dir = os.path.dirname(__file__)
    json_file = os.path.join(current_dir, 'stations.json')

    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Обработка полученного JSON
    for station in data:
        name = station['name']
        code = station['code']
        territory = station['territory']

        result_ter = await session.execute(select(Territory).filter_by(code=territory))
        class_ter = result_ter.scalar_one_or_none()
        territory_id = class_ter.id if class_ter else None

        result = await session.execute(select(Station).filter(Station.code == code))
        obj = result.scalars().first()
        if not obj:
            new_station = Station(
                code=code,
                territory_id=territory_id,
                name=name
            )
            session.add(new_station)
    await session.commit()


# Загружаем роды ПС
async def load_wagon_types(session):
    current_dir = os.path.dirname(__file__)
    json_file = os.path.join(current_dir, 'wagon_types.json')

    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Обработка полученного JSON
    for type_data in data:
        name = type_data['name']
        code = type_data['code']
        platform = type_data['platform']
        official_name = type_data['official_name']

        result = await session.execute(select(WagonType).filter(WagonType.name == name))
        obj = result.scalars().first()
        if not obj:
            new_wagon_type = WagonType(
                code=str(code),
                platform=platform,
                official_name=official_name,
                name=name
            )
            session.add(new_wagon_type)
    await session.commit()


# Загружаем грузы по ЕТСНГ
async def load_etsn(session):
    current_dir = os.path.dirname(__file__)
    json_file = os.path.join(current_dir, 'ETSNG.json')

    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Обработка полученного JSON
    for str_data in data:
        name = str_data['name']
        code = str(str_data['code'])

        result = await session.execute(select(Etsng).filter(Etsng.code == code))
        obj = result.scalars().first()
        if not obj:
            new_obj = Etsng(
                code=code,
                name=name
            )
            session.add(new_obj)
    await session.commit()


# Загружаем грузы по ГНГ
async def load_gng(session):
    current_dir = os.path.dirname(__file__)
    json_file = os.path.join(current_dir, 'GNG.json')

    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Обработка полученного JSON
    for str_data in data:
        name = str_data['name']
        code = str(str_data['code'])

        result = await session.execute(select(Gng).filter(Gng.code == code))
        obj = result.scalars().first()
        if not obj:
            new_obj = Gng(
                code=code,
                name=name
            )
            session.add(new_obj)
    await session.commit()
