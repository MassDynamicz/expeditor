from pydantic import BaseModel
from datetime import datetime, date
from decimal import Decimal
from typing import Optional


class ContractBase(BaseModel):
    name: str
    guid: Optional[str] = None
    number: Optional[str] = None
    from_date: Optional[date] = None
    to_date: Optional[date] = None
    organization_id: int
    contractor_id: int
    currency_id: int

    class Config:
        from_attributes = True


class ContractInDB(ContractBase):
    id: int

    class Config:
        from_attributes = True
