from pydantic import BaseModel
from typing import Optional


class WagonTypeBase(BaseModel):
    name: str
    code: str
    official_name: Optional[str] = None
    key_names: Optional[str] = None
    platform: bool

    class Config:
        from_attributes = True


class WagonTypeInDB(WagonTypeBase):
    id: int

    class Config:
        from_attributes = True
