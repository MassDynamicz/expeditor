from pydantic import BaseModel
from typing import Optional
from datetime import date


class BankAccountBase(BaseModel):
    name: str
    guid: Optional[str] = None
    number: str
    number: str
    organization_id: Optional[int] = None
    contractor_id: Optional[int] = None
    currency_id: int
    bank_id: int

    class Config:
        from_attributes = True


class BankAccountInDB(BankAccountBase):
    id: int

    class Config:
        from_attributes = True
