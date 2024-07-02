from pydantic import BaseModel
from typing import Optional


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
        orm_mode = True
        from_attributes = True


class Country(CountryInDBBase):
    pass


class CountryInDB(CountryInDBBase):
    pass
# endregion
