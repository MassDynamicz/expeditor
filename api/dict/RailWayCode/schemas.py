from pydantic import BaseModel
from typing import Optional


class RailWayCodeBase(BaseModel):
    name: str
    code: Optional[str] = None
    owner_id: int
    territory_id: int

    class Config:
        from_attributes = True


class RailWayCodeInDB(RailWayCodeBase):
    id: int

    class Config:
        from_attributes = True
