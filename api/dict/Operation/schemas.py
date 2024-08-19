from pydantic import BaseModel
from typing import Optional


class OperationBase(BaseModel):
    name: str
    code: Optional[str] = None
    vat_id: int

    class Config:
        from_attributes = True


class OperationInDB(OperationBase):
    id: int

    class Config:
        from_attributes = True
