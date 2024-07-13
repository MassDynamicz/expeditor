from pydantic import BaseModel
from typing import Optional
from api.dict.Territory.schemas import TerritoryInDBBase


# region Схема НДС
class StationBase(BaseModel):
    name: str
    code: str
    territory_id: int
    latitude: Optional[str] = ""
    longitude: Optional[str] = ""

class StationCreate(StationBase):
    pass


class StationUpdate(BaseModel):
    name: str
    code: str
    territory_id: int
    latitude: Optional[str] = ""
    longitude: Optional[str] = ""

class StationInDBBase(StationBase):
    id: int

    class Config:
        from_attributes = True


class StationRelate(StationBase):
    id: int
    territory_data: TerritoryInDBBase

    class Config:
        from_attributes = True


class Station(StationInDBBase):
    pass


class StationInDB(StationInDBBase):
    pass
# endregion
