from pydantic import BaseModel
from datetime import datetime
from decimal import Decimal
from typing import Optional


class CountryBase(BaseModel):
    name: str
    guid: Optional[str] = None
    full_name: str
    code: str

    class Config:
        from_attributes = True


class CountryInDB(CountryBase):
    id: int

    class Config:
        from_attributes = True
