from pydantic import BaseModel
from typing import Optional


class ServiceTypeBase(BaseModel):
    name: str

    class Config:
        from_attributes = True


class ServiceTypeInDB(ServiceTypeBase):
    id: int

    class Config:
        from_attributes = True
