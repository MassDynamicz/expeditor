from pydantic import BaseModel
from datetime import datetime
from decimal import Decimal
from typing import Optional


class CurrencyBase(BaseModel):
    name: str
    guid: Optional[str] = None
    code: str

    class Config:
        from_attributes = True


class CurrencyInDB(CurrencyBase):
    id: int

    class Config:
        from_attributes = True
