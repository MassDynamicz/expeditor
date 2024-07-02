from pydantic import BaseModel
from typing import Optional
from api.dict.WagonType.schemas import WagonTypeInDBBase


# region Схема НДС
class WagonBase(BaseModel):
    name: str
    wagon_type_id: Optional[int] = None


class WagonCreate(WagonBase):
    pass


class WagonUpdate(BaseModel):
    name: str
    wagon_type_id: Optional[int] = None


class WagonInDBBase(WagonBase):
    id: int

    class Config:
        orm_mode = True
        from_attributes = True


class WagonRelate(WagonBase):
    id: int
    wagon_type_data: Optional[WagonTypeInDBBase] = None

    class Config:
        orm_mode = True
        from_attributes = True


class Wagon(WagonInDBBase):
    pass


class WagonInDB(WagonInDBBase):
    pass
# endregion
