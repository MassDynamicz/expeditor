from pydantic import BaseModel, conint, Field
from typing import Optional


# region Схема НДС
class EtsngBase(BaseModel):
    name: str
    code: str


class EtsngCreate(EtsngBase):
    pass


class EtsngUpdate(BaseModel):
    name: str
    code: str


class EtsngInDBBase(EtsngBase):
    id: int

    class Config:
        from_attributes = True


class Etsng(EtsngInDBBase):
    pass


class EtsngInDB(EtsngInDBBase):
    pass
# endregion
