from pydantic import BaseModel
from typing import Optional
from datetime import date


class ContractBase(BaseModel):
    name: str
    guid: Optional[str] = None
    number: str
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
