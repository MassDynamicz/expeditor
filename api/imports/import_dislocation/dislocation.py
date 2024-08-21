import html
from datetime import date
import httpx
from fastapi import HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from api.dict.Wagon.models import Wagon
from api.dict.Station.models import Station
from api.dict.Territory.models import Territory
from api.dict.Container.models import Container
from api.dict.Etsng.models import Etsng
from api.doc.Dislocation.models import Dislocation
from config.utils import format_date as parse_date


async def load_dislocation(request: Request, session: AsyncSession):
    json_data = await fetch_railwagon_data()
    if json_data:
        try:
            async with session.begin():
                for vagon in json_data["vagon"]:
                    await parse_vagon_data(vagon, session)
        except Exception as e:
            await session.rollback()
            raise HTTPException(status_code=500, detail=str(e))
        else:
            await session.commit()
        return {"status": "success"}
    else:
        raise HTTPException(status_code=400, detail="Не удалось получить данные")


async def fetch_railwagon_data():
    url = 'https://railwagonlocation.com:443/xml/export.php'
    name = 'SSGM LogisticsApi'
    password = 'DsTMQPpJ'

    params = {
        'name': name,
        'password': password,
        'request_type': 'get_user_vagons',
        'all_operations': 'n',
        'added_last_minutes': '60',
        'return_format': 'json'
    }

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params, headers=headers)
            response.raise_for_status()
            return response.json()
    except httpx.HTTPStatusError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')
    return None


async def parse_vagon_data(vagon_data, session: AsyncSession):
    cur_date = date.today()
    vagon_info = vagon_data["vagon_info"]
    vagon_position = vagon_data["position"]

    vagon_or_container = vagon_info['@attributes']['type']
    is_container = vagon_or_container != "vagon"

    container_array = []

    if not is_container:
        owner = html.unescape(vagon_info['vagon_specifications']['owner'])
        owner_code = vagon_info['vagon_specifications']['owner_code']
        next_repair = parse_date(vagon_info['vagon_specifications']['next_repair_date'])
        next_repair_type = vagon_info['vagon_specifications']['next_repair_type']
        vagon_no = vagon_info["vagon_no"]

        if "containers" in vagon_position:
            if isinstance(vagon_position["containers"]["container"], list):
                for cont in vagon_position["containers"]["container"]:
                    container_array.append(cont["@attributes"]['no'])
            else:
                container_array.append(vagon_position["containers"]["container"]["@attributes"]['no'])
        else:
            container_array.append('')
    else:
        owner = ''
        owner_code = ''
        next_repair = None
        next_repair_type = ''
        vagon_no = vagon_info["platform_no"]
        container_array.append(vagon_info["vagon_no"])

    wagon = await get_wagon(session, vagon_no)

    date_otpr = parse_date(vagon_info["send_date"])
    date_otpr_time = parse_date(vagon_info["send_date_time"])
    date_oper = parse_date(vagon_position['current_position_date'])
    date_arrive = parse_date(vagon_info["arrive_date_real"] if isinstance(vagon_info['arrive_date_real'], str) else '')
    date_arrive_plan = parse_date(vagon_info["arrive_date"] if isinstance(vagon_info['arrive_date'], str) else '')
    loaded = vagon_position['loaded'] == 'y'
    nomer_nakladnoi = vagon_position['nomer_nakladnoi'] if isinstance(vagon_position['nomer_nakladnoi'], str) else ''
    operation = vagon_position["operation"] if isinstance(vagon_position["operation"], str) else ''
    operation_id = vagon_position["operation_id"] if isinstance(vagon_position["operation_id"], str) else ''
    operation_code = vagon_position["operation_code"] if isinstance(vagon_position["operation_code"], str) else ''
    broken = vagon_position["broken"] == 'y'
    group_name = vagon_info["group_name"] if isinstance(vagon_info["group_name"], str) else ''
    group_id = vagon_info["group_id"] if isinstance(vagon_info["group_id"], str) else ''
    gruz_sender = html.unescape(
        vagon_position["gruz_sender_name"] if isinstance(vagon_position['gruz_sender_name'], str) else '')
    gruz_receiver = html.unescape(
        vagon_position["gruz_receiver_name"] if isinstance(vagon_position['gruz_receiver_name'], str) else '')
    payer = ''
    vagon_comment = vagon_info['vagon_comment'] if isinstance(vagon_info['vagon_comment'], str) else ''

    weight = await parse_numeric(session, vagon_position["weight"])
    distance_end = await parse_numeric(session, vagon_position["distance_end"])
    distance_full = await parse_numeric(session, vagon_position["full_distance"])
    days_wo_movement = await parse_numeric(session, vagon_info['days_wo_movement'])
    days_wo_operation = await parse_numeric(session, vagon_info['days_wo_operation'])
    days_in_transit = await parse_numeric(session, vagon_info['days_in_transit'])

    station_otpr = await get_station(session, vagon_info["from_code"], vagon_info["from_name"],
                                     vagon_info["from_latitude"], vagon_info["from_longitude"])
    station_tek = await get_station(session, vagon_position["current_position_code"],
                                    vagon_position["current_position"], vagon_position["current_position_latitude"],
                                    vagon_position["current_position_longitude"])
    station_nazn = await get_station(session, vagon_info["to_code"], vagon_info["to_name"], vagon_info["to_latitude"],
                                     vagon_info["to_longitude"])

    etnsng = await get_etsng(session, vagon_position["etsng_code"], vagon_position["state"])
    prev_etsng = await get_etsng(session, vagon_position["previous_etsng"]["@attributes"]["code"],
                                 vagon_position["previous_etsng"]["name"])

    for cont in container_array:
        model_cont = await get_container(session, cont)

        dislocation = Dislocation(
            date=cur_date,
            wagon_id=wagon,
            container_id=model_cont,
            loaded=loaded,
            nomer_nakladnoi=nomer_nakladnoi,
            date_otpr=date_otpr,
            date_otpr_time=date_otpr_time,
            date_oper=date_oper,
            date_arrive=date_arrive,
            date_arrive_plan=date_arrive_plan,
            station_otpr_id=station_otpr,
            station_tek_id=station_tek,
            station_nazn_id=station_nazn,
            operation=operation,
            operation_id=operation_id,
            operation_code=operation_code,
            broken=broken,
            weight=weight,
            etsng_id=etnsng,
            prev_etsng_id=prev_etsng,
            distance_end=distance_end,
            distance_full=distance_full,
            group_name=group_name,
            group_id=group_id,
            gruz_sender=gruz_sender,
            gruz_receiver=gruz_receiver,
            payer=payer,
            owner=owner,
            owner_code=owner_code,
            next_repair=next_repair,
            next_repair_type=next_repair_type,
            days_wo_movement=days_wo_movement,
            days_wo_operation=days_wo_operation,
            days_in_transit=days_in_transit,
            vagon_comment=vagon_comment)
        session.add(dislocation)

    return {"status": "SUCCESS"}


async def get_station(session: AsyncSession, st_code, st_name, latitude, longitude):
    result = await session.execute(select(Station).filter(Station.code == st_code))
    station = result.scalars().first()
    if not station:
        result = await session.execute(select(Territory).filter(Territory.code == '0000'))
        territory = result.scalars().first()
        if not territory:
            territory = Territory(code='0000', name='НЕОПРЕДЕЛЕНО')
            session.add(territory)
            await session.flush()
            await session.refresh(territory)
        station = Station(name=st_name, code=st_code, territory=territory, latitude=latitude, longitude=longitude)
        session.add(station)
        await session.flush()
        await session.refresh(station)
    else:
        if not station.latitude or not station.longitude:
            station.latitude = latitude
            station.longitude = longitude
            await session.flush()
    return station.id


async def parse_numeric(session: AsyncSession, state):
    if not isinstance(state, str):
        return 0
    if state == '':
        return 0
    try:
        return int(state)
    except ValueError:
        try:
            return float(state)
        except ValueError:
            return 0


async def get_etsng(session: AsyncSession, etsgn_code, state):
    if not isinstance(etsgn_code, str):
        return None

    if etsgn_code == '':
        return None

    result = await session.execute(select(Etsng).filter(Etsng.code == etsgn_code))
    etsng = result.scalars().first()
    if not etsng:
        etsng = Etsng(name=state, code=etsgn_code)
        session.add(etsng)
        await session.flush()
        await session.refresh(etsng)
    return etsng.id


async def get_wagon(session: AsyncSession, name):
    if name == '' or not isinstance(name, str):
        return None

    result = await session.execute(select(Wagon).filter(Wagon.name == name))
    obj = result.scalars().first()
    if not obj:
        obj = Wagon(name=name)
        session.add(obj)
        await session.flush()
        await session.refresh(obj)
    return obj.id


async def get_container(session: AsyncSession, name):
    if name == '' or not isinstance(name, str):
        return None

    result = await session.execute(select(Container).filter(Container.name == name))
    obj = result.scalars().first()
    if not obj:
        obj = Container(name=name)
        session.add(obj)
        await session.flush()
        await session.refresh(obj)
    return obj.id
