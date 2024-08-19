from pydantic import BaseModel
from typing import Optional


class ContractorBase(BaseModel):
    name: str
    guid: Optional[str] = None
    full_name: Optional[str] = None
    bin: Optional[str] = None
    kbe: Optional[str] = None
    enterpreneur: bool
    legal_address: Optional[str] = None
    legal_entity: bool
    country_id: int
    comment: Optional[str] = None
    document: Optional[str] = None

    class Config:
        from_attributes = True


class ContractorInDB(ContractorBase):
    id: int

    class Config:
        from_attributes = True
