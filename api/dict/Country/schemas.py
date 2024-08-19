from pydantic import BaseModel
from typing import Optional


class CountryBase(BaseModel):
    name: str
    guid: Optional[str] = None
    code: str
    full_name: str
    code: str

    class Config:
        from_attributes = True


class CountryInDB(CountryBase):
    id: int

    class Config:
        from_attributes = True
