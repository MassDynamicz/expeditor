from pydantic import BaseModel
from datetime import datetime
from decimal import Decimal
from typing import Optional

from api.dict.OwnerType.models import OwnerType


class OrganizationBase(BaseModel):
    name: str
    guid: Optional[str] = None
    full_name: str
    bin: str
    kbe: str
    enterpreneur: bool
    legal_address: str
    owner_type: OwnerType
    country_id: int

    class Config:
        from_attributes = True


class OrganizationInDB(OrganizationBase):
    id: int

    class Config:
        from_attributes = True
