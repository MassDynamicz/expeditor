from pydantic import BaseModel
from typing import Optional


class BankBase(BaseModel):
    name: str
    guid: Optional[str] = None
    bik: Optional[str] = None
    city: Optional[str] = None

    class Config:
        from_attributes = True


class BankInDB(BankBase):
    id: int

    class Config:
        from_attributes = True

