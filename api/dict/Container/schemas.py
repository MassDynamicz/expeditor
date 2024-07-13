from pydantic import BaseModel
from typing import Optional
from api.dict.WagonType.schemas import WagonTypeInDBBase


# region Схема НДС
class ContainerBase(BaseModel):
    name: str
    wagon_type_id: Optional[int] = None


class ContainerCreate(ContainerBase):
    pass


class ContainerUpdate(BaseModel):
    name: str
    wagon_type_id: Optional[int] = None


class ContainerInDBBase(ContainerBase):
    id: int

    class Config:
        from_attributes = True


class ContainerRelate(ContainerBase):
    id: int
    wagon_type_data: Optional[WagonTypeInDBBase] = None

    class Config:
        from_attributes = True


class Container(ContainerInDBBase):
    pass


class ContainerInDB(ContainerInDBBase):
    pass
# endregion
