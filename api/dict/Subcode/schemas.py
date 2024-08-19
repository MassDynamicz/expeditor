from pydantic import BaseModel
from typing import Optional


class SubcodeBase(BaseModel):
    name: str
    owner_id: int

    class Config:
        from_attributes = True


class SubcodeInDB(SubcodeBase):
    id: int

    class Config:
        from_attributes = True
