from pydantic import BaseModel
from typing import Optional
from api.dict.Organization.schemas import OrganizationInDBBase
from api.dict.Currency.schemas import CurrencyInDBBase
from api.dict.Bank.schemas import BankInDBBase


# region
class BankAccountOrgBase(BaseModel):
    name: str
    guid: Optional[str] = ""
    number: str
    currency_id: int
    bank_id: int
    owner_id: int


class BankAccountOrgCreate(BankAccountOrgBase):
    pass


class BankAccountOrgUpdate(BaseModel):
    name: str
    guid: Optional[str] = ""
    number: str
    currency_id: int
    bank_id: int
    owner_id: int


class BankAccountOrgInDBBase(BankAccountOrgBase):
    id: int

    class Config:
        from_attributes = True


class BankAccountOrgRelate(BankAccountOrgBase):
    id: int
    currency_data: CurrencyInDBBase
    bank_data: BankInDBBase
    owner_data: OrganizationInDBBase

    class Config:
        from_attributes = True


class BankAccountOrg(BankAccountOrgInDBBase):
    pass


class BankAccountOrgInDB(BankAccountOrgInDBBase):
    pass
# endregion
