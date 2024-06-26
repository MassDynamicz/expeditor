from pydantic import BaseModel
from typing import Optional


# region Схема валюты
class CurrencyBase(BaseModel):
    name: str
    guid: Optional[str] = ""
    code: str
    copybook_parameters_ru: Optional[str] = ""
    copybook_parameters_en: Optional[str] = ""


class CurrencyCreate(CurrencyBase):
    pass


class CurrencyUpdate(BaseModel):
    name: str = None
    guid: str = None
    code: str = None
    copybook_parameters_ru: str = None
    copybook_parameters_en: str = None


class CurrencyInDBBase(CurrencyBase):
    id: int

    class Config:
        from_attributes = True


class Currency(CurrencyInDBBase):
    pass


class CurrencyInDB(CurrencyInDBBase):
    pass
# endregion


# region Схема страна
class CountryBase(BaseModel):
    name: str
    guid: Optional[str] = ""
    code: str
    full_name: Optional[str] = ""


class CountryCreate(CountryBase):
    pass


class CountryUpdate(BaseModel):
    name: str = None
    guid: str = None
    code: str = None
    full_name: str = None


class CountryInDBBase(CountryBase):
    id: int

    class Config:
        from_attributes = True


class Country(CountryInDBBase):
    pass


class CountryInDB(CountryInDBBase):
    pass
# endregion
