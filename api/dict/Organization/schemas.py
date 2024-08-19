from pydantic import BaseModel
from typing import Optional


class OrganizationBase(BaseModel):
    name: str
    guid: Optional[str] = None
    full_name: Optional[str] = None
    bin: Optional[str] = None
    kbe: Optional[str] = None
    enterpreneur: bool
    legal_address: Optional[str] = None
    legal_entity: bool
    country_id: int

    class Config:
        from_attributes = True


class OrganizationInDB(OrganizationBase):
    id: int

    class Config:
        from_attributes = True
