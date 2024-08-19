from pydantic import BaseModel
from typing import Optional


class CurrencyBase(BaseModel):
    name: str
    guid: Optional[str] = None
    code: str
    copybook_parameters_ru: Optional[str] = None
    copybook_parameters_en: Optional[str] = None

    class Config:
        from_attributes = True


class CurrencyInDB(CurrencyBase):
    id: int

    class Config:
        from_attributes = True
