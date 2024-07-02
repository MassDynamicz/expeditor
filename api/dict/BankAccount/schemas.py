from pydantic import BaseModel
from typing import Optional
from api.dict.Contractor.schemas import ContractorInDB
from api.dict.Currency.schemas import CurrencyInDBBase
from api.dict.Bank.schemas import BankInDBBase


# region Схема НДС
class BankAccountBase(BaseModel):
    name: str
    guid: Optional[str] = ""
    number: str
    currency_id: int
    bank_id: int
    owner_id: int


class BankAccountCreate(BankAccountBase):
    pass


class BankAccountUpdate(BaseModel):
    name: str
    guid: Optional[str] = ""
    number: str
    currency_id: int
    bank_id: int
    owner_id: int


class BankAccountInDBBase(BankAccountBase):
    id: int

    class Config:
        orm_mode = True
        from_attributes = True


class BankAccountRelate(BankAccountBase):
    id: int
    currency_data: CurrencyInDBBase
    bank_data: BankInDBBase
    owner_data: ContractorInDB

    class Config:
        orm_mode = True
        from_attributes = True


class BankAccount(BankAccountInDBBase):
    pass


class BankAccountInDB(BankAccountInDBBase):
    pass
# endregion
