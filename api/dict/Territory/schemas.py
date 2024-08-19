from pydantic import BaseModel
from typing import Optional


class TerritoryBase(BaseModel):
    name: str
    code: str


class TerritoryInDB(TerritoryBase):
    id: int

    class Config:
        from_attributes = True
