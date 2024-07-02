from pydantic import BaseModel
from typing import Optional
from api.dict.Vat.schemas import VatInDBBase


# region Схема НДС
class OperationBase(BaseModel):
    name: str
    code: Optional[str] = ""
    vat_id: Optional[int] = None


class OperationCreate(OperationBase):
    pass


class OperationUpdate(BaseModel):
    name: str
    code: str = None
    vat_id: int = None


class OperationInDBBase(OperationBase):
    id: int

    class Config:
        orm_mode = True
        from_attributes = True


class OperationRelate(OperationBase):
    id: int
    vat_data: Optional[VatInDBBase] = None

    class Config:
        orm_mode = True
        from_attributes = True


class Operation(OperationInDBBase):
    pass


class OperationInDB(OperationInDBBase):
    pass
# endregion
