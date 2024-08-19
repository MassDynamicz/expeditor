from pydantic import BaseModel
from typing import Optional


class EtsngBase(BaseModel):
    name: str
    code: str


class EtsngInDB(EtsngBase):
    id: int

    class Config:
        from_attributes = True
