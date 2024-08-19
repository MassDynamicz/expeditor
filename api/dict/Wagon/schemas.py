from pydantic import BaseModel
from typing import Optional


class WagonBase(BaseModel):
    name: str
    wagon_type_id: Optional[int] = None

    class Config:
        from_attributes = True


class WagonInDB(WagonBase):
    id: int

    class Config:
        from_attributes = True
