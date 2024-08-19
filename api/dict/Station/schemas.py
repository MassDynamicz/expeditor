from pydantic import BaseModel
from typing import Optional


class StationBase(BaseModel):
    name: str
    code: str
    latitude: Optional[str] = None
    longitude: Optional[str] = None
    territory_id: int

    class Config:
        from_attributes = True


class StationInDB(StationBase):
    id: int

    class Config:
        from_attributes = True
