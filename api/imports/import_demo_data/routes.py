from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime

from api.auth.models import User
from api.dict.Bank.models import Bank
from api.dict.BankAccount.models import BankAccount
from api.dict.Container.models import Container
from api.dict.Contract.models import Contract
from api.dict.Contractor.models import Contractor
from api.dict.Country.models import Country
from api.dict.Currency.models import Currency
from api.dict.Operation.models import Operation
from api.dict.Organization.models import Organization
from api.dict.ServiceType.models import ServiceType
from api.dict.Vat.models import Vat
from api.dict.Wagon.models import Wagon
from api.dict.WagonType.models import WagonType
from api.doc.OrderRailWay.models import OrderRailWay
from api.imports.import_dicts_for_rail_way.data_rw import load_rw_json
from config.db import get_db


router = APIRouter()


async def load_currencies(session):
    new_obj = Currency(
        name="KZT",
        guid=None,
        code="398",
        copybook_parameters_ru=None,
        copybook_parameters_en=None
    )
    session.add(new_obj)

    new_obj = Currency(
        name="USD",
        guid=None,
        code="840",
        copybook_parameters_ru=None,
        copybook_parameters_en=None
    )
    session.add(new_obj)

    new_obj = Currency(
        name="EUR",
        guid=None,
        code="978",
        copybook_parameters_ru=None,
        copybook_parameters_en=None
    )
    session.add(new_obj)
    await session.commit()
    return None


async def load_banks(session):
    new_obj = Bank(
        name="KASPI BANK",
        guid=None,
        bik="CASPKZKA",
        city="Алматы"
    )
    session.add(new_obj)

    new_obj = Bank(
        name="Банк ЦентрКредит",
        guid=None,
        bik="KCJBKZKX",
        city="Алматы"
    )
    session.add(new_obj)

    new_obj = Bank(
        name="Народный Банк Казахстана",
        guid=None,
        bik="HSBKKZKX",
        city="Алматы"
    )
    session.add(new_obj)

    await session.commit()
    return None


async def load_vat(session):
    new_obj = Vat(
        name="12%",
        guid=None,
        rate=12
    )
    session.add(new_obj)

    new_obj = Vat(
        name="Без НДС",
        guid=None,
        rate=0
    )
    session.add(new_obj)

    new_obj = Vat(
        name="0%",
        guid=None,
        rate=0
    )
    session.add(new_obj)

    await session.commit()
    return None


async def load_countries(session):
    new_obj = Country(
        name="Казахстан",
        guid=None,
        full_name="Республика Казахстан",
        code="KZ"
    )
    session.add(new_obj)

    new_obj = Country(
        name="Россия",
        guid=None,
        full_name="Российская Федерация",
        code="RU"
    )
    session.add(new_obj)

    new_obj = Country(
        name="Узбекистан",
        guid=None,
        full_name="Республика Узбекистан",
        code="UZ"
    )
    session.add(new_obj)

    await session.commit()
    return None


async def load_organization(session):
    result = await session.execute(select(Country))
    country = result.scalars().first()

    result = await session.execute(select(Bank))
    bank = result.scalars().first()

    result = await session.execute(select(Currency))
    currency = result.scalars().first()

    new_obj = Organization(
        name="Airo System",
        guid=None,
        full_name="Товарищество с ограниченной ответственностью \"Airo System\"",
        bin="160840016234",
        kbe="17",
        enterpreneur=False,
        legal_address="Казахстан, г. Алматы, Ауэзовский район, Микрорайон 9, дом 35А, индекс 050010",
        legal_entity=True,
        country_id=country.id
    )
    session.add(new_obj)
    await session.flush()

    new_ba = BankAccount(
        name="Расчетный счет организации",
        guid=None,
        number="KZ82722S000016738626",
        currency_id=currency.id,
        bank_id=bank.id,
        contractor_id=None,
        organization_id=new_obj.id
    )
    session.add(new_ba)

    await session.commit()
    return None


async def load_wagons(session):
    result = await session.execute(select(WagonType))
    wagon_t = result.scalars().first()

    new_obj = Wagon(
        name="29005469",
        wagon_type_id=wagon_t.id
    )
    session.add(new_obj)

    new_obj = Wagon(
        name="29074697",
        wagon_type_id=wagon_t.id
    )
    session.add(new_obj)

    new_obj = Wagon(
        name="29146396",
        wagon_type_id=wagon_t.id
    )
    session.add(new_obj)

    new_obj = Wagon(
        name="29185899",
        wagon_type_id=wagon_t.id
    )
    session.add(new_obj)

    new_obj = Wagon(
        name="29226347",
        wagon_type_id=wagon_t.id
    )
    session.add(new_obj)

    await session.commit()
    return None


async def load_containers(session):
    result = await session.execute(select(WagonType))
    wagon_t = result.scalars().first()

    new_obj = Container(
        name="TCKU9521103",
        wagon_type_id=wagon_t.id
    )
    session.add(new_obj)

    new_obj = Container(
        name="DFSU2123796",
        wagon_type_id=wagon_t.id
    )
    session.add(new_obj)

    new_obj = Container(
        name="HLXU2375559",
        wagon_type_id=wagon_t.id
    )
    session.add(new_obj)

    new_obj = Container(
        name="DFSU2393169",
        wagon_type_id=wagon_t.id
    )
    session.add(new_obj)

    new_obj = Container(
        name="JZPU2104912",
        wagon_type_id=wagon_t.id
    )
    session.add(new_obj)

    await session.commit()
    return None


async def load_service_types(session):
    new_obj = ServiceType(
        name="Экспедирование"
    )
    session.add(new_obj)

    new_obj = ServiceType(
        name="Предоставление ПС"
    )
    session.add(new_obj)

    new_obj = ServiceType(
        name="Экспедирование + Предоставление ПС"
    )
    session.add(new_obj)

    await session.commit()
    return None


async def load_operations(session):
    result = await session.execute(select(Vat))
    vat = result.scalars().first()

    new_obj = Operation(
        name="Предоставление ПС",
        code=None,
        vat_id=vat.id
    )
    session.add(new_obj)

    new_obj = Operation(
        name="Тариф внутри КЗХ",
        code=None,
        vat_id=vat.id
    )
    session.add(new_obj)

    new_obj = Operation(
        name="Транзит КЗХ",
        code=None,
        vat_id=vat.id
    )
    session.add(new_obj)

    await session.commit()
    return None


async def load_contractors(session):
    result = await session.execute(select(Country))
    country = result.scalars().first()

    result = await session.execute(select(Organization))
    org = result.scalars().first()

    result = await session.execute(select(Currency))
    currency = result.scalars().first()

    result = await session.execute(select(Bank))
    bank = result.scalars().first()

    new_obj = Contractor(
        name="SSGM Logistics",
        guid=None,
        full_name="Товарищество с ограниченной ответственностью \"SSGM Logistics\"",
        bin="230240047238",
        kbe="17",
        enterpreneur=False,
        legal_address="Казахстан, г. Алматы, Бостандыкский район, улица Абиш Кекилбайулы, здание 1, индекс 050000",
        legal_entity=True,
        comment=None,
        document=None,
        country_id=country.id
    )
    session.add(new_obj)
    await session.flush()
    new_contract = Contract(
        name="Договор №1 от 01.01.2024г.",
        guid=None,
        number="1",
        from_date=datetime.strptime("2024-01-01", "%Y-%m-%d").date(),
        to_date=datetime.strptime("2024-12-31", "%Y-%m-%d").date(),
        organization_id=org.id,
        contractor_id=new_obj.id,
        currency_id=currency.id
    )
    session.add(new_contract)
    new_ba = BankAccount(
        name="Расчетный счет контрагента",
        guid=None,
        number="KZ00000S000000000001",
        currency_id=currency.id,
        bank_id=bank.id,
        contractor_id=new_obj.id,
        organization_id=None
    )
    session.add(new_ba)

    new_obj = Contractor(
        name="КТЖ-Грузовые перевозки ТОО",
        guid=None,
        full_name="Товарищество с ограниченной ответственностью \"КТЖ-Грузовые перевозки\"",
        bin="031040001799",
        kbe="17",
        enterpreneur=False,
        legal_address="Казахстан, г. Нур-Султан, 010000, район Есиль, ул. Д. Кунаева, 10",
        legal_entity=True,
        comment=None,
        document=None,
        country_id=country.id
    )
    session.add(new_obj)
    await session.flush()
    new_contract = Contract(
        name="Договор №2 от 01.01.2024г.",
        guid=None,
        number="2",
        from_date=datetime.strptime("2024-01-01", "%Y-%m-%d").date(),
        to_date=datetime.strptime("2024-12-31", "%Y-%m-%d").date(),
        organization_id=org.id,
        contractor_id=new_obj.id,
        currency_id=currency.id
    )
    session.add(new_contract)
    new_ba = BankAccount(
        name="Расчетный счет контрагента",
        guid=None,
        number="KZ00000S000000000001",
        currency_id=currency.id,
        bank_id=bank.id,
        contractor_id=new_obj.id,
        organization_id=None
    )
    session.add(new_ba)

    new_obj = Contractor(
        name="Кедентранссервис АО",
        guid=None,
        full_name="Кедентранссервис АО",
        bin="990840000825",
        kbe="17",
        enterpreneur=False,
        legal_address="Республика Казахстан, 010016, г. Нур-Султан, Есильский район, улица Достык,18",
        legal_entity=True,
        comment=None,
        document=None,
        country_id=country.id
    )
    session.add(new_obj)
    await session.flush()
    new_contract = Contract(
        name="Договор №3 от 01.01.2024г.",
        guid=None,
        number="3",
        from_date=datetime.strptime("2024-01-01", "%Y-%m-%d").date(),
        to_date=datetime.strptime("2024-12-31", "%Y-%m-%d").date(),
        organization_id=org.id,
        contractor_id=new_obj.id,
        currency_id=currency.id
    )
    session.add(new_contract)
    new_ba = BankAccount(
        name="Расчетный счет контрагента",
        guid=None,
        number="KZ00000S000000000001",
        currency_id=currency.id,
        bank_id=bank.id,
        contractor_id=new_obj.id,
        organization_id=None
    )
    session.add(new_ba)

    await session.commit()
    return None


async def load_orders(session):
    result = await session.execute(select(Organization))
    org = result.scalars().first()

    result = await session.execute(select(User))
    user = result.scalars().first()

    result = await session.execute(select(Contractor))
    contractor = result.scalars().first()

    result = await session.execute(select(ServiceType))
    service = result.scalars().first()

    result = await session.execute(select(Contract).filter(Contract.contractor_id == contractor.id))
    contract = result.scalars().first()

    for _ in range(100):
        new_obj = OrderRailWay(
            date=datetime.strptime("2024-08-24", "%Y-%m-%d").date(),
            comment="test",
            sum=1000,
            amount=2,
            rate=1,
            confirmed=False,
            organization_id=org.id,
            author_id=user.id,
            manager_id=user.id,
            client_id=contractor.id,
            contract_id=contract.id,
            service_type_id=service.id
        )
        session.add(new_obj)

    await session.commit()
    return None


@router.post("/")
async def import_rail_way_dicts(db: AsyncSession = Depends(get_db)):
    try:
        rw = await load_rw_json(db)
        currencies = await load_currencies(db)
        banks = await load_banks(db)
        vat = await load_vat(db)
        countries = await load_countries(db)
        org = await load_organization(db)
        wagons = await load_wagons(db)
        containers = await load_containers(db)
        st = await load_service_types(db)
        operations = await load_operations(db)
        contractor = await load_contractors(db)
        orders = await load_orders(db)
        return {"status": "SUCCESS"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to import demo data: {str(e)}")
