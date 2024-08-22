from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime
import os
import json
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
from config.db import get_db
from config.utils import format_date as parse_date


router = APIRouter()


async def load_currencies(data, session):
    name = data['name']
    guid = data['guid']
    code = data['code']

    result = await session.execute(select(Currency).filter(Currency.guid == guid))
    obj = result.scalars().first()

    if not obj:
        new_obj = Currency(
            name=name,
            guid=guid,
            code=code
        )
        session.add(new_obj)
    await session.commit()
    return None


async def load_banks(data, session):
    name = data['name']
    guid = data['guid']
    bik = data['bik']
    city = data['city']

    result = await session.execute(select(Bank).filter(Bank.guid == guid))
    obj = result.scalars().first()

    if not obj:
        new_obj = Bank(
            name=name,
            guid=guid,
            bik=bik,
            city=city
        )
        session.add(new_obj)
    await session.commit()
    return None


async def load_vat(data, session):
    name = data['name']
    guid = data['guid']
    rate = data['rate']

    result = await session.execute(select(Vat).filter(Vat.guid == guid))
    obj = result.scalars().first()

    if not obj:
        new_obj = Vat(
            name=name,
            guid=guid,
            rate=rate
        )
        session.add(new_obj)
    await session.commit()
    return None


async def load_countries(data, session):
    name = data['name']
    guid = data['guid']
    full_name = data['full_name']
    code = data['code']

    result = await session.execute(select(Country).filter(Country.guid == guid))
    obj = result.scalars().first()

    if not obj:
        new_obj = Country(
            name=name,
            guid=guid,
            full_name=full_name,
            code=code
        )
        session.add(new_obj)
    await session.commit()
    return None


async def load_organization(data, session):
    name = data['name']
    guid = data['guid']
    full_name = data['full_name']
    bin_iin = data['bin']
    kbe = data['kbe']
    country = data['country']
    enterpreneur = True
    legal_entity = True
    legal_address = data['legal_address']
    country = data['country']

    result_country = await session.execute(select(Country).filter(Country.name == "Казахстан"))
    country_obj = result_country.scalars().first()

    result = await session.execute(select(Organization).filter(Organization.guid == guid))
    obj = result.scalars().first()

    if not obj:
        new_obj = Organization(
            name=name,
            guid=guid,
            full_name=full_name,
            bin=bin_iin,
            kbe=kbe,
            enterpreneur=enterpreneur,
            legal_address=legal_address,
            legal_entity=legal_entity,
            country_id=country_obj.id
        )
        session.add(new_obj)
    await session.commit()
    return None


async def load_wagons(data, session):
    name = data['name']

    result = await session.execute(select(Wagon).filter(Wagon.name == name))
    obj = result.scalars().first()

    if not obj:
        new_obj = Wagon(
            name=name,
            wagon_type_id=None
        )
        session.add(new_obj)
    await session.commit()
    return None


async def load_containers(data, session):
    container_name = data['name']

    result = await session.execute(select(Container).filter(Container.name == container_name))
    obj = result.scalars().first()

    if not obj:
        new_obj = Container(
            name=container_name,
            wagon_type_id=None
        )
        session.add(new_obj)
    await session.commit()
    return None


async def load_service_types(data, session):
    name = data['name']

    result = await session.execute(select(ServiceType).filter(ServiceType.name == name))
    obj = result.scalars().first()

    if not obj:
        new_obj = ServiceType(
            name=name
        )
        session.add(new_obj)
    await session.commit()
    return None


async def load_operations(data, session):
    name = data['name']
    vat = data['vat']

    result_vat = await session.execute(select(Vat).filter(Vat.guid == vat))
    vat_obj = result_vat.scalars().first()

    result = await session.execute(select(Operation).filter(Operation.name == name))
    obj = result.scalars().first()

    if not obj:
        new_obj = Operation(
            name=name,
            code=None,
            vat_id=vat_obj.id
        )
        session.add(new_obj)
    await session.commit()
    return None


async def load_contractors(data, session):
    name = data['name']
    guid = data['guid']
    full_name = data['full_name']
    bin_iin = data['bin']
    kbe = data['kbe']
    country = data['country']
    enterpreneur = data['enterpreneur']
    legal_entity = data['legal_entity']
    legal_address = data['legal_address']
    comment = data['comment']
    document = data['document']
    country = data['country']

    result_country = await session.execute(select(Country).filter(Country.guid == country))
    country_obj = result_country.scalars().first()
    if not country_obj:
        result_country = await session.execute(select(Country).filter(Country.name == "Казахстан"))
        country_obj = result_country.scalars().first()

    result = await session.execute(select(Contractor).filter(Contractor.guid == guid))
    obj = result.scalars().first()

    if not obj:
        new_obj = Contractor(
            name=name,
            guid=guid,
            full_name=full_name,
            bin=bin_iin,
            kbe=kbe,
            enterpreneur=enterpreneur,
            legal_address=legal_address,
            legal_entity=legal_entity,
            country_id=country_obj.id,
            comment=comment,
            document=document
        )
        session.add(new_obj)
    await session.commit()
    return None


async def load_bank_account_org(data, session):
    name = data['name']
    guid = data['guid']
    number = data['number']
    currency = data['currency']
    bank = data['bank']
    owner = data['owner']

    result_owner = await session.execute(select(Organization).filter(Organization.guid == owner))
    owner_obj = result_owner.scalars().first()

    result_bank = await session.execute(select(Bank).filter(Bank.guid == bank))
    bank_obj = result_bank.scalars().first()

    result_currency = await session.execute(select(Currency).filter(Currency.guid == currency))
    currency_obj = result_currency.scalars().first()
    if not currency_obj:
        return None

    result = await session.execute(select(BankAccount).filter(BankAccount.guid == guid))
    obj = result.scalars().first()

    if not obj:
        new_obj = BankAccount(
            name=name,
            guid=guid,
            number=number,
            currency_id=currency_obj.id,
            bank_id=bank_obj.id,
            organization_id=owner_obj.id,
            contractor_id=None
        )
        session.add(new_obj)
    await session.commit()
    return None


async def load_bank_account_cont(data, session):
    name = data['name']
    guid = data['guid']
    number = data['number']
    currency = data['currency']
    bank = data['bank']
    owner = data['owner']

    result_owner = await session.execute(select(Contractor).filter(Contractor.guid == owner))
    owner_obj = result_owner.scalars().first()

    result_bank = await session.execute(select(Bank).filter(Bank.guid == bank))
    bank_obj = result_bank.scalars().first()

    result_currency = await session.execute(select(Currency).filter(Currency.guid == currency))
    currency_obj = result_currency.scalars().first()

    result = await session.execute(select(BankAccount).filter(BankAccount.guid == guid))
    obj = result.scalars().first()

    if not obj:
        new_obj = BankAccount(
            name=name,
            guid=guid,
            number=number,
            currency_id=currency_obj.id,
            bank_id=bank_obj.id,
            organization_id=None,
            contractor_id=owner_obj.id
        )
        session.add(new_obj)
    await session.commit()
    return None


async def load_contracts(data, session):
    name = data['name']
    guid = data['guid']
    organization = data['organization']
    number = data['number']
    contractor = data['contractor']
    currency = data['currency']
    from_date = parse_date(data['from_date'])
    to_date = parse_date(data['to_date'])

    result_org = await session.execute(select(Organization).filter(Organization.guid == organization))
    org_obj = result_org.scalars().first()

    result_contractor = await session.execute(select(Contractor).filter(Contractor.guid == contractor))
    contractor_obj = result_contractor.scalars().first()

    result_currency = await session.execute(select(Currency).filter(Currency.guid == currency))
    currency_obj = result_currency.scalars().first()
    if not currency_obj:
        return None

    result = await session.execute(select(Contract).filter(Contract.guid == guid))
    obj = result.scalars().first()

    if not obj:
        new_obj = Contract(
            name=name,
            guid=guid,
            number=number,
            from_date=from_date,
            to_date=to_date,
            organization_id=org_obj.id,
            contractor_id=contractor_obj.id,
            currency_id=currency_obj.id
        )
        session.add(new_obj)
    await session.commit()
    return None


async def load_orders(data, session):
    date = parse_date(data['date'])
    comment = data['comment']
    summ = data['sum']
    amount = data['amount']
    rate = data['rate']
    confirmed = data['confirmed']
    organization = data['organization']
    client = data['client']
    contract = data['contract']
    service_type = data['service_type']
    number = data['number']

    result_org = await session.execute(select(Organization).filter(Organization.guid == organization))
    org_obj = result_org.scalars().first()

    result_client = await session.execute(select(Contractor).filter(Contractor.guid == client))
    client_obj = result_client.scalars().first()

    result_contract = await session.execute(select(Contract).filter(Contract.guid == contract))
    contract_obj = result_contract.scalars().first()

    result_st = await session.execute(select(ServiceType).filter(ServiceType.name == service_type))
    st_obj = result_st.scalars().first()

    result = await session.execute(select(OrderRailWay).filter(OrderRailWay.number == number))
    obj = result.scalars().first()

    if not obj:
        new_obj = OrderRailWay(
            date=date,
            number=number,
            comment=comment,
            sum=summ,
            amount=amount,
            rate=rate,
            confirmed=confirmed,
            organization_id=org_obj.id,
            author_id=1,
            manager_id=1,
            client_id=client_obj.id,
            contract_id=contract_obj.id,
            service_type_id=st_obj.id
        )
        session.add(new_obj)
    await session.commit()
    return None



@router.post("/")
async def import_rail_way_dicts(db: AsyncSession = Depends(get_db)):
    try:
        current_dir = os.path.dirname(__file__)
        json_file = os.path.join(current_dir, 'demo_data.json')

        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            for container in data["Container"]:
                await load_containers(container, db)
            for vat in data["NDS"]:
                await load_vat(vat, db)
            for currency in data["Currency"]:
                await load_currencies(currency, db)
            for country in data["Country"]:
                await load_countries(country, db)
            for bank in data["Bank"]:
                await load_banks(bank, db)
            for org in data["Organization"]:
                await load_organization(org, db)
            for contractor in data["Contractor"]:
                await load_contractors(contractor, db)
            for bank_account_org in data["BankAccountOrg"]:
                await load_bank_account_org(bank_account_org, db)
            for bank_account in data["BankAccount"]:
                await load_bank_account_cont(bank_account, db)
            for contract in data["Contract"]:
                await load_contracts(contract, db)
            for wagon in data["Wagon"]:
                await load_wagons(wagon, db)
            for operation in data["Operation"]:
                await load_operations(operation, db)
            for service_type in data["ServiceType"]:
                await load_service_types(service_type, db)
            for order in data["OrderRailWay"]:
                await load_orders(order, db)

        return {"status": "SUCCESS"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to import demo data: {str(e)}")
