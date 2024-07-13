from pydantic import BaseModel
from typing import Optional

from api.dict.OwnerType.models import OwnerType
from api.dict.Country.schemas import CountryInDBBase


# region Схема организации
class OrganizationBase(BaseModel):
    name: str
    guid: Optional[str] = ""
    full_name: Optional[str] = ""
    bin: str
    kbe: Optional[str] = ""
    enterpreneur: bool = False
    legal_address: Optional[str] = ""
    owner_type: OwnerType
    country_id: Optional[int] = None


class OrganizationCreate(OrganizationBase):
    pass


class OrganizationUpdate(BaseModel):
    name: str = None
    guid: str = None
    full_name: str = None
    bin: str = None
    kbe: str = None
    enterpreneur: bool = False
    legal_address: str = None
    owner_type: OwnerType = "Entity"
    country_id: Optional[int] = None


class OrganizationInDBBase(OrganizationBase):
    id: int

    class Config:
        from_attributes = True


class OrganizationRelate(OrganizationBase):
    id: int
    country_data: Optional[CountryInDBBase] = None

    class Config:
        from_attributes = True


class Organization(OrganizationInDBBase):
    pass


class OrganizationInDB(OrganizationInDBBase):
    pass
# endregion
