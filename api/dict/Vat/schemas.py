from pydantic import BaseModel, conint, Field
from typing import Optional


# region Схема НДС
class VatBase(BaseModel):
    name: str
    guid: Optional[str] = ""
    rate: conint(ge=0, le=100) = Field(..., description="Rate must be an integer between 0 and 100")


class VatCreate(VatBase):
    pass


class VatUpdate(BaseModel):
    name: str = None
    guid: str = None
    rate: str = None


class VatInDBBase(VatBase):
    id: int

    class Config:
        from_attributes = True


class Vat(VatInDBBase):
    pass


class VatInDB(VatInDBBase):
    pass
# endregion
