import enum
from sqlalchemy import Column, Integer, String, Boolean, Date, ForeignKey, Numeric, Enum, event
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import relationship, Session, InstrumentedAttribute
from config.db import Base


# Класс - валюта
class Currency(Base):
    __tablename__ = "currencies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False)
    guid = Column(String(100), default="")
    code = Column(String(3), nullable=False)
    copybook_parameters_ru = Column(String(200), default="")
    copybook_parameters_en = Column(String(200), default="")

    bank_accounts = relationship("BankAccount", back_populates="currency")
    bank_accounts_org = relationship("BankAccountOrg", back_populates="currency")
    contracts = relationship("Contract", back_populates="currency")

    def __repr__(self):
        return f"'{self.name}'"


# Класс - ставка НДС
class Vat(Base):
    __tablename__ = "vat"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False)
    guid = Column(String(100), default="")
    rate = Column(Numeric(15, 4), default=0)

    operations = relationship("Operation", back_populates="vat")

    def __repr__(self):
        return f"'{self.name}'"


# Класс - Банк
class Bank(Base):
    __tablename__ = "banks"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False)
    guid = Column(String(100), default="")
    bik = Column(String(50), default="")
    city = Column(String(100), default="")

    bank_accounts = relationship("BankAccount", back_populates="bank")
    bank_accounts_org = relationship("BankAccountOrg", back_populates="bank")

    def __repr__(self):
        return f"'{self.name}'"


# Класс - Страна
class Country(Base):
    __tablename__ = "countries"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False)
    guid = Column(String(100), default="")
    full_name = Column(String(300), default="")
    code = Column(String(5), nullable=False)

    organizations = relationship("Organization", back_populates="country")
    contractors = relationship("Contractor", back_populates="country")

    def __repr__(self):
        return f"'{self.name}'"


# Перечисление - виды собственности
class OwnerType(enum.Enum):
    # Физ лицо
    Individual = "Individual"
    # Юр. лицо
    Entity = "Entity"


# Класс - Организация
class Organization(Base):
    __tablename__ = "organizations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False)
    guid = Column(String(100), default="")
    full_name = Column(String(300), default="")
    bin = Column(String(15), nullable=False)
    kbe = Column(String(10), default="")
    enterpreneur = Column(Boolean, default=False)
    legal_address = Column(String(300), default="")
    owner_type = Column(Enum(OwnerType), nullable=False)
    country_id = Column(Integer, ForeignKey('countries.id'), nullable=True)

    # Определяем отношение
    country = relationship("Country", back_populates="organizations")
    contracts = relationship("Contract", back_populates="organization")
    bank_accounts_org = relationship("BankAccountOrg", back_populates="owner")

    def __repr__(self):
        return f"'{self.name}'"


# Класс - Контрагент
class Contractor(Base):
    __tablename__ = "contractors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False)
    guid = Column(String(100), default="")
    full_name = Column(String(300), default="")
    bin = Column(String(15), nullable=False)
    kbe = Column(String(10), default="")
    enterpreneur = Column(Boolean, default=False)
    legal_address = Column(String(300), default="")
    comment = Column(String(300), default="")
    document = Column(String(300), default="")
    owner_type = Column(Enum(OwnerType), nullable=False)
    country_id = Column(Integer, ForeignKey('countries.id'), nullable=True)

    # Определяем отношение
    country = relationship("Country", back_populates="contractors")
    contracts = relationship("Contract", back_populates="contractor")
    bank_accounts = relationship("BankAccount", back_populates="owner")

    def __repr__(self):
        return f"'{self.name}'"


# Класс - Договора
class Contract(Base):
    __tablename__ = "contracts"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False)
    guid = Column(String(100), default="")
    number = Column(String(150), default="")
    from_date = Column(Date)
    to_date = Column(Date)
    organization_id = Column(Integer, ForeignKey('organizations.id'), nullable=False)
    contractor_id = Column(Integer, ForeignKey('contractors.id'), nullable=False)
    currency_id = Column(Integer, ForeignKey('currencies.id'), nullable=False)

    organization = relationship("Organization", back_populates="contracts")
    contractor = relationship("Contractor", back_populates="contracts")
    currency = relationship("Currency", back_populates="contracts")

    def __repr__(self):
        return f"'{self.name}'"


# Класс - Банковские счета контрагентов
class BankAccount(Base):
    __tablename__ = "bank_accounts"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False)
    guid = Column(String(100), default="")
    number = Column(String(150), default="")
    currency_id = Column(Integer, ForeignKey('currencies.id'), nullable=False)
    bank_id = Column(Integer, ForeignKey('banks.id'), nullable=False)
    owner_id = Column(Integer, ForeignKey('contractors.id'), nullable=False)

    currency = relationship("Currency", back_populates="bank_accounts")
    bank = relationship("Bank", back_populates="bank_accounts")
    owner = relationship("Contractor", back_populates="bank_accounts")

    def __repr__(self):
        return f"'{self.name}'"


# Класс - Банковские счета организации
class BankAccountOrg(Base):
    __tablename__ = "bank_accounts_org"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False)
    guid = Column(String(100), default="")
    number = Column(String(150), default="")
    currency_id = Column(Integer, ForeignKey('currencies.id'), nullable=False)
    bank_id = Column(Integer, ForeignKey('banks.id'), nullable=False)
    owner_id = Column(Integer, ForeignKey('organizations.id'), nullable=False)

    currency = relationship("Currency", back_populates="bank_accounts_org")
    bank = relationship("Bank", back_populates="bank_accounts_org")
    owner = relationship("Organization", back_populates="bank_accounts_org")

    def __repr__(self):
        return f"'{self.name}'"


# Класс - ЖД территории
class Territory(Base):
    __tablename__ = "territories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False)
    code = Column(String(10), nullable=False)

    stations = relationship("Station", back_populates="territory")

    def __repr__(self):
        return f"'{self.name}'"


# Класс - ЖД станции
class Station(Base):
    __tablename__ = "stations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False)
    code = Column(String(20), unique=True, nullable=False)
    territory_id = Column(Integer, ForeignKey('territories.id'), nullable=False)
    territory = relationship("Territory", back_populates="stations")
    latitude = Column(String(100), default='')
    longitude = Column(String(100), default='')

    def __repr__(self):
        return f"'{self.name}'"


# Класс - Роды подвижного состава
class WagonType(Base):
    __tablename__ = "wagon_types"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False)
    code = Column(String(20), unique=True, nullable=False)
    official_name = Column(String(300), default='')
    key_names = Column(String(500), default='')
    platform = Column(Boolean, default=False)

    wagons = relationship("Wagon", back_populates="wagon_type")
    containers = relationship("Container", back_populates="wagon_type")

    def __repr__(self):
        return f"'{self.name}'"


# Класс - Вагон
class Wagon(Base):
    __tablename__ = "wagons"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(20), nullable=False)
    wagon_type_id = Column(Integer, ForeignKey('wagon_types.id'), default=0)
    wagon_type = relationship("WagonType", back_populates="wagons")

    def __repr__(self):
        return f"'{self.name}'"


# Класс - Вагон
class Container(Base):
    __tablename__ = "containers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(20), nullable=False)
    wagon_type_id = Column(Integer, ForeignKey('wagon_types.id'), default=0)
    wagon_type = relationship("WagonType", back_populates="containers")

    def __repr__(self):
        return f"'{self.name}'"


# Класс - ЕТСНГ
class Etsng(Base):
    __tablename__ = "etsng"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    code = Column(String(20), unique=True, nullable=False)

    def __repr__(self):
        return f"'{self.name}'"


# Класс - ГНГ
class Gng(Base):
    __tablename__ = "gng"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    code = Column(String(20), unique=True, nullable=False)
    code_etsng = Column(String(20), unique=True, nullable=False)

    def __repr__(self):
        return f"'{self.name}'"


# Класс - Операции
class Operation(Base):
    __tablename__ = "operations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    code = Column(String(20), default='')
    vat_id = Column(Integer, ForeignKey('vat.id'), default=0)
    vat = relationship("Vat", back_populates="operations")

    def __repr__(self):
        return f"'{self.name}'"


# Класс - Виды услуг
class ServiceType(Base):
    __tablename__ = "service_types"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)

    def __repr__(self):
        return f"'{self.name}'"


# Событие для защиты удаления записи во всех таблицах с ForeignKey
@event.listens_for(Session, "before_flush")
def protect_delete_foreignkey(session, flush_context, instances):
    for instance in session.deleted:
        # Итерируемся по всем атрибутам модели
        for key, value in instance.__mapper__.all_orm_descriptors.items():
            if isinstance(value, InstrumentedAttribute) and value.prop.columns[0].foreign_keys:
                # Проверка наличия связанных записей
                related_model = value.prop.mapper.class_
                related_records = session.query(related_model).filter(value == instance.id).count()
                if related_records > 0:
                    raise IntegrityError(
                        f"Cannot delete {instance} because it has related records in {related_model}.",
                        "protect_delete_foreignkey",
                        instance
                    )
