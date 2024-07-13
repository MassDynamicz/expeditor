from datetime import date
from pydantic import BaseModel
from typing import Optional
from api.dict.Contractor.schemas import ContractorInDBBase
from api.dict.Contract.schemas import ContractInDBBase
from api.dict.Organization.schemas import OrganizationInDBBase
from api.dict.ServiceType.schemas import ServiceTypeInDBBase
from api.auth.schemas import User
from decimal import Decimal


class OrderRWBase(BaseModel):
    date: date
    comment: Optional[str] = ""
    rate: Decimal
    organization_id: int
    author_id: int
    manager_id: int
    client_id: int
    contract_id: int
    service_type_id: int


class OrderRWCreate(OrderRWBase):
    pass


class OrderRWUpdate(BaseModel):
    date: date
    rate: Decimal
    comment: str = ""
    organization_id: int
    author_id: int
    manager_id: int
    client_id: int
    contract_id: int
    service_type_id: int


class OrderRWInDBBase(OrderRWBase):
    id: int

    class Config:
        from_attributes = True


class OrderRWRelate(OrderRWBase):
    id: int
    sum: Decimal
    amount: int
    organization_data: OrganizationInDBBase
    client_data: ContractorInDBBase
    contract_data: ContractInDBBase
    author_data: User
    manager_data: User
    service_type_data: ServiceTypeInDBBase

    class Config:
        from_attributes = True


class OrderRW(OrderRWInDBBase):
    pass


class OrderRWInDB(OrderRWInDBBase):
    pass
