from pydantic import BaseModel
from datetime import datetime
from decimal import Decimal
from typing import Optional
from api.dict.OwnerType.models import OwnerType


class ContractorBase(BaseModel):
    name: str
    guid: Optional[str] = None
    full_name: str
    bin: str
    kbe: str
    enterpreneur: bool
    legal_address: str
    comment: str
    document: str
    owner_type: OwnerType
    country_id: int

    class Config:
        from_attributes = True


class ContractorInDB(ContractorBase):
    id: int

    class Config:
        from_attributes = True
