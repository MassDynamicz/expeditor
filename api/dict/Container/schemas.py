from pydantic import BaseModel
from typing import Optional


class ContainerBase(BaseModel):
    name: str
    wagon_type_id: Optional[int] = None

    class Config:
        from_attributes = True


class ContainerInDB(ContainerBase):
    id: int

    class Config:
        from_attributes = True
