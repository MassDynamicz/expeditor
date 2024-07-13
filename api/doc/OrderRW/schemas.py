from datetime import datetime, date
from pydantic import BaseModel

from api.dict.Container.schemas import ContainerInDBBase
from api.dict.Contractor.schemas import ContractorInDBBase
from api.dict.Contract.schemas import ContractInDBBase
from api.dict.Currency.schemas import CurrencyInDBBase
from api.dict.Etsng.schemas import EtsngInDBBase
from api.dict.Gng.schemas import GngInDBBase
from api.dict.Operation.schemas import OperationInDBBase
from api.dict.Organization.schemas import OrganizationInDBBase
from api.dict.ServiceType.schemas import ServiceTypeInDBBase
from api.auth.schemas import User
from decimal import Decimal
from api.dict.Station.schemas import StationInDBBase
from api.dict.Subcode.schemas import SubcodeInDBBase
from api.dict.Vat.schemas import VatInDBBase
from api.dict.Wagon.schemas import WagonInDBBase
from api.dict.WagonType.schemas import WagonTypeInDBBase
from typing import Optional


# Схема заявки
class ORWBase(BaseModel):
    date: datetime
    comment: str
    rate: Decimal
    sum: Decimal
    amount: int
    organization_id: int
    author_id: int
    manager_id: int
    client_id: int
    contract_id: int
    service_type_id: int
    confirmed: bool

    class Config:
        from_attributes = True


class ORWRead(ORWBase):
    id: int
    organization_data: OrganizationInDBBase
    client_data: ContractorInDBBase
    contract_data: ContractInDBBase
    author_data: User
    manager_data: User
    service_type_data: ServiceTypeInDBBase

    class Config:
        from_attributes = True


class ORWCreate(ORWBase):

    class Config:
        from_attributes = True


class ORWUpdate(BaseModel):
    date: Optional[datetime] = None
    comment: Optional[str] = None
    rate: Optional[Decimal] = None
    sum: Optional[Decimal] = None
    amount: Optional[int] = None
    organization_id: Optional[int] = None
    author_id: Optional[int] = None
    manager_id: Optional[int] = None
    client_id: Optional[int] = None
    contract_id: Optional[int] = None
    service_type_id: Optional[int] = None
    confirmed: Optional[bool] = None

    class Config:
        from_attributes = True


class ORW_id(ORWBase):
    id: int

    class Config:
        from_attributes = True


# Маршруты заявки
class ORWRouteBase(BaseModel):
    weight: Decimal
    amount: int
    price: Decimal
    sum: Decimal
    comment: str
    orderrw_id: int
    station_otpr_id: int
    station_nazn_id: int
    wagon_type_id: int
    etsng_id: int
    gng_id: int
    vat_id: int


class ORWRouteRead(ORWRouteBase):
    id: int
    orderrw_data: ORWBase
    station_otpr_data: StationInDBBase
    station_nazn_data: StationInDBBase
    wagon_type_data: WagonTypeInDBBase
    etsng_data: EtsngInDBBase
    gng_data: GngInDBBase

    class Config:
        from_attributes = True


class ORWRouteUpdate(BaseModel):
    weight: Optional[Decimal] = None
    amount: Optional[int] = None
    price: Optional[Decimal] = None
    sum: Optional[Decimal] = None
    comment: Optional[str] = None
    orderrw_id: Optional[int] = None
    station_otpr_id: Optional[int] = None
    station_nazn_id: Optional[int] = None
    wagon_type_id: Optional[int] = None
    etsng_id: Optional[int] = None
    gng_id: Optional[int] = None
    vat_id: Optional[int] = None

    class Config:
        from_attributes = True


class ORWRouteCreate(ORWRouteBase):

    class Config:
        from_attributes = True


class ORWRoute_id(BaseModel):
    id: int

    class Config:
        from_attributes = True


# Перевозки
class ORWTransportBase(BaseModel):
    date_otpr: Optional[date] = None
    date_otpr_sng: Optional[date] = None
    date_transshipment: Optional[date] = None
    date_arrive: Optional[date] = None
    date_arrive_border: Optional[date] = None
    profit: Decimal
    comment: Optional[str] = None
    td: Optional[str] = None
    rate: Decimal
    otpr_number: Optional[str] = None
    sum: Decimal
    weight: Decimal
    orderrw_id: int
    station_otpr_id: int
    station_nazn_id: int
    wagon_id: Optional[int] = None
    wagon_cn_id: Optional[int] = None
    container_id: Optional[int] = None
    subcode1_id: Optional[int] = None
    subcode2_id: Optional[int] = None
    subcode3_id: Optional[int] = None
    subcode4_id: Optional[int] = None
    subcode5_id: Optional[int] = None
    etsng_id: Optional[int] = None
    gng_id: Optional[int] = None
    wagon_type_id: Optional[int] = None
    vat_id: int


class ORWTransportRead(ORWTransportBase):
    id: int
    station_otpr_data: StationInDBBase
    station_nazn_data: StationInDBBase
    wagon_data: Optional[WagonInDBBase] = None
    wagon_cn_data: Optional[WagonInDBBase] = None
    container_data: Optional[ContainerInDBBase] = None
    subcode1_data: Optional[SubcodeInDBBase] = None
    subcode2_data: Optional[SubcodeInDBBase] = None
    subcode3_data: Optional[SubcodeInDBBase] = None
    subcode4_data: Optional[SubcodeInDBBase] = None
    subcode5_data: Optional[SubcodeInDBBase] = None
    etsng_data: Optional[EtsngInDBBase] = None
    gng_data: Optional[GngInDBBase] = None
    wagon_type_data: WagonTypeInDBBase
    vat_data: VatInDBBase

    class Config:
        from_attributes = True


class ORWTransportUpdate(BaseModel):
    date_otpr: Optional[date] = None
    date_otpr_sng: Optional[date] = None
    date_transshipment: Optional[date] = None
    date_arrive: Optional[date] = None
    date_arrive_border: Optional[date] = None
    profit: Optional[Decimal] = None
    comment: Optional[str] = None
    td: Optional[str] = None
    rate: Optional[Decimal] = None
    otpr_number: Optional[str] = None
    sum: Optional[Decimal] = None
    weight: Optional[Decimal] = None
    orderrw_id: Optional[int] = None
    station_otpr_id: Optional[int] = None
    station_nazn_id: Optional[int] = None
    wagon_id: Optional[int] = None
    wagon_cn_id: Optional[int] = None
    container_id: Optional[int] = None
    subcode1_id: Optional[int] = None
    subcode2_id: Optional[int] = None
    subcode3_id: Optional[int] = None
    subcode4_id: Optional[int] = None
    subcode5_id: Optional[int] = None
    etsng_id: Optional[int] = None
    gng_id: Optional[int] = None
    wagon_type_id: Optional[int] = None
    vat_id: Optional[int] = None

    class Config:
        from_attributes = True


class ORWTransportCreate(ORWTransportBase):

    class Config:
        from_attributes = True


class ORWTransport_id(BaseModel):
    id: int

    class Config:
        from_attributes = True


# Поставщики
class ORWProviderBase(BaseModel):
    rate: Decimal
    sum_plan: Decimal
    sum_fact: Decimal
    card_number: Optional[str] = None
    scroll: Optional[str] = None
    provider_id: int
    contract_id: int
    currency_id: int
    operation_id: int
    vat_id: int


class ORWProviderRead(ORWProviderBase):
    id: int
    provider_data: ContractorInDBBase
    contract_data: ContractInDBBase
    currency_data: CurrencyInDBBase
    operation_data: OperationInDBBase
    vat_data: VatInDBBase

    class Config:
        from_attributes = True


class ORWProviderUpdate(BaseModel):
    rate: Optional[Decimal] = None
    sum_plan: Optional[Decimal] = None
    sum_fact: Optional[Decimal] = None
    card_number: Optional[str] = None
    scroll: Optional[str] = None
    provider_id: Optional[int] = None
    contract_id: Optional[int] = None
    currency_id: Optional[int] = None
    operation_id: Optional[int] = None
    vat_id: Optional[int] = None

    class Config:
        from_attributes = True


class ORWProviderCreate(ORWProviderBase):

    class Config:
        from_attributes = True


class ORWProvider_id(BaseModel):
    id: int

    class Config:
        from_attributes = True
