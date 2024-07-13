from pydantic import BaseModel
from typing import Optional


# region Банк
class BankBase(BaseModel):
    name: str
    guid: Optional[str] = ""
    bik: Optional[str] = ""
    city: Optional[str] = ""

class BankCreate(BankBase):
    pass


class BankUpdate(BaseModel):
    name: str = None
    guid: str = None
    bik: str = None
    city: str = None


class BankInDBBase(BankBase):
    id: int

    class Config:
        from_attributes = True


class Bank(BankInDBBase):
    pass


class BankInDB(BankInDBBase):
    pass
# endregion
