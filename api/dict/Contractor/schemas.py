from pydantic import BaseModel
from typing import Optional
from api.dict.OwnerType.models import OwnerType
from api.dict.Country.schemas import CountryInDBBase


# region Схема НДС
class ContractorBase(BaseModel):
    name: str
    guid: Optional[str] = ""
    full_name: Optional[str] = ""
    bin: Optional[str] = ""
    kbe: Optional[str] = ""
    enterpreneur: bool = False
    legal_address: Optional[str] = ""
    comment: Optional[str] = ""
    document: Optional[str] = ""
    owner_type: OwnerType
    country_id: Optional[int] = None


class ContractorCreate(ContractorBase):
    pass


class ContractorUpdate(BaseModel):
    name: str = None
    guid: str = None
    full_name: str = None
    bin: str = None
    kbe: str = None
    enterpreneur: bool = False
    legal_address: str = None
    comment: str = None
    document: str = None
    owner_type: OwnerType = "Entity"
    country_id: Optional[int] = None


class ContractorInDBBase(ContractorBase):
    id: int

    class Config:
        from_attributes = True


class ContractorRelate(ContractorBase):
    id: int
    country_data: Optional[CountryInDBBase] = None

    class Config:
        from_attributes = True


class Contractor(ContractorInDBBase):
    pass


class ContractorInDB(ContractorInDBBase):
    pass
# endregion
