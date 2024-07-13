from datetime import date

from pydantic import BaseModel
from typing import Optional

from api.dict.Contractor.schemas import ContractorInDBBase
from api.dict.Currency.schemas import CurrencyInDBBase
from api.dict.Organization.schemas import OrganizationInDBBase


# region Схема НДС
class ContractBase(BaseModel):
    name: str
    guid: Optional[str] = ""
    number: str
    from_date: Optional[date] = None
    to_date: Optional[date] = None
    organization_id: int
    contractor_id: int
    currency_id: int


class ContractCreate(ContractBase):
    pass


class ContractUpdate(BaseModel):
    name: str
    guid: str = None
    number: str
    from_date: date = None
    to_date: date = None
    organization_id: int
    contractor_id: int
    currency_id: int


class ContractInDBBase(ContractBase):
    id: int

    class Config:
        from_attributes = True


class ContractRelate(ContractBase):
    id: int
    organization_data: OrganizationInDBBase
    contractor_data: ContractorInDBBase
    currency_data: CurrencyInDBBase

    class Config:
        from_attributes = True


class Contract(ContractInDBBase):
    pass


class ContractInDB(ContractInDBBase):
    pass
# endregion
