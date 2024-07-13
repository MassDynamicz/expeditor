from pydantic import BaseModel, conint, Field
from typing import Optional


class WagonTypeBase(BaseModel):
    name: str
    code: Optional[str] = ""
    official_name: Optional[str] = ""
    key_names: Optional[str] = ""
    platform: Optional[bool] = False


class WagonTypeCreate(WagonTypeBase):
    pass


class WagonTypeUpdate(BaseModel):
    name: str
    code: str = None
    official_name: str = None
    key_names: str = None
    platform: bool = False


class WagonTypeInDBBase(WagonTypeBase):
    id: int

    class Config:
        from_attributes = True


class WagonType(WagonTypeInDBBase):
    pass


class WagonTypeInDB(WagonTypeInDBBase):
    pass
