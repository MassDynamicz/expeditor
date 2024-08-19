from pydantic import BaseModel
from typing import Optional


class VatBase(BaseModel):
    name: str
    guid: Optional[str] = None
    rate: int
    class Config:
        from_attributes = True


class VatInDB(VatBase):
    id: int

    class Config:
        from_attributes = True
