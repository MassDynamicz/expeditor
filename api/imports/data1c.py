from fastapi import Request
import json
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from datetime import datetime, date
from api.dict.Bank.models import Bank
from api.dict.BankAccount.models import BankAccount
from api.dict.BankAccountOrg.models import BankAccountOrg
from api.dict.Contract.models import Contract
from api.dict.Contractor.models import Contractor
from api.dict.Currency.models import Currency
from api.dict.Country.models import Country
from api.dict.Organization.models import Organization
from api.dict.Vat.models import Vat
from typing import Optional


async def receive_json_1c(request: Request, session: AsyncSession):
    try:
        data = await request.json()
        # Обработка полученного JSON
        await load_currency(session, data)
        await load_countries(session, data)
        await load_vat(session, data)
        await load_banks(session, data)
        await load_organizations(session, data)
        await load_contractors(session, data)
        await load_bank_accounts_org(session, data)
        await load_bank_accounts(session, data)
        await load_contracts(session, data)
        return {"message": "JSON received successfully", "status": "OK"}
    except json.JSONDecodeError:
        return {"error": "Invalid JSON", "status": "ERROR"}


async def load_currency(session, data):
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
    await session.commit()


async def load_countries(session, data):
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


async def load_vat(session, data):
    for vat_data in data.get('NDS', []):
        guid = vat_data['guid']
        result = await session.execute(select(Vat).filter_by(guid=guid))
        existing_vat = result.scalar_one_or_none()
        if existing_vat:
            # Обновляем существующий объект
            for key, value in vat_data.items():
                setattr(existing_vat, key, value)
        else:
            # Создаем новый объект
            new_vat = Vat(**vat_data)
            session.add(new_vat)
    await session.commit()


async def load_banks(session, data):
    for bank_data in data.get('Bank', []):
        guid = bank_data['guid']
        result = await session.execute(select(Bank).filter_by(guid=guid))
        existing_bank = result.scalar_one_or_none()
        if existing_bank:
            # Обновляем существующий объект
            for key, value in bank_data.items():
                setattr(existing_bank, key, value)
        else:
            # Создаем новый объект
            new_bank = Bank(**bank_data)
            session.add(new_bank)
    await session.commit()


async def load_organizations(session, data):
    for org_data in data.get('Organization', []):
        guid = org_data['guid']
        name = org_data['name']
        full_name = org_data['full_name']
        bin_iin = org_data['bin']
        kbe = org_data['kbe']
        owner_type = org_data['owner_type']
        enterpreneur = org_data['enterpreneur']
        legal_address = org_data['legal_address']

        country_code = org_data['country']
        result_country = await session.execute(select(Country).filter_by(code=country_code))
        country = result_country.scalar_one_or_none()
        country_id = country.id if country else None

        result = await session.execute(select(Organization).filter(Organization.guid == guid))
        org = result.scalars().first()
        if org:
            org.name = name
            org.full_name = full_name
            org.bin = bin_iin
            org.kbe = kbe
            org.country_id = country_id
            org.owner_type = owner_type
            org.enterpreneur = enterpreneur
            org.legal_address = legal_address
        else:
            # Создаем новый объект
            new_org = Organization(
                guid=guid,
                name=name,
                full_name=full_name,
                bin=bin_iin,
                kbe=kbe,
                country_id=country_id,
                owner_type=owner_type,
                enterpreneur=enterpreneur,
                legal_address=legal_address
            )
            session.add(new_org)
    await session.commit()


async def load_contractors(session, data):
    # Загружаем контрагентов
    for contractor_data in data.get('Contractor', []):
        name = contractor_data['name']
        guid = contractor_data['guid']
        full_name = contractor_data['full_name']
        bin_iin = contractor_data['bin']
        kbe = contractor_data['kbe']
        owner_type = contractor_data['owner_type']
        enterpreneur = contractor_data['enterpreneur']
        legal_address = contractor_data['legal_address']
        comment = contractor_data['comment']
        document = contractor_data['document']

        country_guid = contractor_data['country']
        result_country = await session.execute(select(Country).filter_by(guid=country_guid))
        country = result_country.scalar_one_or_none()
        country_id = country.id if country else None

        result = await session.execute(select(Contractor).filter(Contractor.guid == guid))
        cont = result.scalars().first()
        if cont:
            cont.name = name
            cont.full_name = full_name
            cont.bin = bin_iin
            cont.kbe = kbe
            cont.country_id = country_id
            cont.owner_type = owner_type
            cont.enterpreneur = enterpreneur
            cont.comment = comment
            cont.document = document
            cont.legal_address = legal_address
        else:
            # Создаем новый объект
            new_contractor = Contractor(
                guid=guid,
                name=name,
                full_name=full_name,
                bin=bin_iin,
                kbe=kbe,
                country_id=country_id,
                owner_type=owner_type,
                enterpreneur=enterpreneur,
                document=document,
                comment=comment,
                legal_address=legal_address
            )
            session.add(new_contractor)
    await session.commit()


async def load_bank_accounts_org(session, data):
    # Загружаем банковские счета организации
    for acc_data in data.get('BankAccountOrg', []):
        name = acc_data['name']
        guid = acc_data['guid']
        number = acc_data['number']
        bank = acc_data['bank']
        owner = acc_data['owner']
        currency = acc_data['currency']

        result_bank = await session.execute(select(Bank).filter_by(guid=bank))
        class_bank = result_bank.scalar_one_or_none()
        bank_id = class_bank.id if class_bank else None

        result_currency = await session.execute(select(Currency).filter_by(guid=currency))
        class_currency = result_currency.scalar_one_or_none()
        currency_id = class_currency.id if class_currency else None

        result_owner = await session.execute(select(Organization).filter_by(guid=owner))
        class_org = result_owner.scalar_one_or_none()
        owner_id = class_org.id if class_org else None

        result = await session.execute(select(BankAccountOrg).filter(BankAccountOrg.guid == guid))
        acc = result.scalars().first()
        if acc:
            acc.name = name
            acc.number = number
            acc.bank_id = bank_id
            acc.currency_id = currency_id
            acc.owner_id = owner_id
        else:
            # Создаем новый объект
            new_acc = BankAccountOrg(
                guid=guid,
                name=name,
                number=number,
                bank_id=bank_id,
                currency_id=currency_id,
                owner_id=owner_id
            )
            session.add(new_acc)
    await session.commit()


async def load_bank_accounts(session, data):
    # Загружаем банковские счета контрагентов
    for acc_data in data.get('BankAccount', []):
        name = acc_data['name']
        guid = acc_data['guid']
        number = acc_data['number']
        bank = acc_data['bank']
        owner = acc_data['owner']
        currency = acc_data['currency']

        result_bank = await session.execute(select(Bank).filter_by(guid=bank))
        class_bank = result_bank.scalar_one_or_none()
        bank_id = class_bank.id if class_bank else None

        result_currency = await session.execute(select(Currency).filter_by(guid=currency))
        class_currency = result_currency.scalar_one_or_none()
        currency_id = class_currency.id if class_currency else None

        result_owner = await session.execute(select(Contractor).filter_by(guid=owner))
        class_org = result_owner.scalar_one_or_none()
        owner_id = class_org.id if class_org else None

        result = await session.execute(select(BankAccount).filter(BankAccount.guid == guid))
        acc = result.scalars().first()
        if acc:
            acc.name = name
            acc.number = number
            acc.bank_id = bank_id
            acc.currency_id = currency_id
            acc.owner_id = owner_id
        else:
            # Создаем новый объект
            new_acc = BankAccount(
                guid=guid,
                name=name,
                number=number,
                bank_id=bank_id,
                currency_id=currency_id,
                owner_id=owner_id
            )
            session.add(new_acc)
    await session.commit()


async def load_contracts (session, data):
    # Загружаем договоры
    for contract_data in data.get('Contract', []):
        name = contract_data['name']
        guid = contract_data['guid']
        number = contract_data['number']
        from_date = contract_data['from_date']
        to_date = contract_data['to_date']
        organization = contract_data['organization']
        contractor = contract_data['contractor']
        currency = contract_data['currency']

        from_date_obj = parse_date(from_date) if from_date else None
        to_date_obj = parse_date(to_date) if to_date else None

        result_currency = await session.execute(select(Currency).filter_by(guid=currency))
        class_currency = result_currency.scalar_one_or_none()
        currency_id = class_currency.id if class_currency else None

        result_org = await session.execute(select(Organization).filter_by(guid=organization))
        class_organization = result_org.scalar_one_or_none()
        organization_id = class_organization.id if class_organization else None

        result_owner = await session.execute(select(Contractor).filter_by(guid=contractor))
        class_contractor = result_owner.scalar_one_or_none()
        contractor_id = class_contractor.id if class_contractor else None

        result = await session.execute(select(Contract).filter(Contract.guid == guid))
        contract = result.scalars().first()
        if contract:
            contract.name = name
            contract.number = number
            contract.from_date = from_date_obj
            contract.to_date = to_date_obj
            contract.organization_id = organization_id
            contract.currency_id = currency_id
            contract.contractor_id = contractor_id
        else:
            # Создаем новый объект
            new_contract = Contract(
                guid=guid,
                name=name,
                number=number,
                from_date=from_date_obj,
                to_date=to_date_obj,
                organization_id=organization_id,
                currency_id=currency_id,
                contractor_id=contractor_id
            )
            session.add(new_contract)
    await session.commit()


def parse_date(date_str: str) -> Optional[date]:
    for fmt in ("%d.%m.%Y", "%Y-%m-%d"):
        try:
            return datetime.strptime(date_str, fmt).date()
        except ValueError:
            pass
    return None
