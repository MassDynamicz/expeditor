from pydantic import BaseModel
from datetime import datetime
from decimal import Decimal
from typing import Optional


class OrderRailWayBase(BaseModel):
    date: datetime
    comment: Optional[str] = None
    sum: Decimal
    amount: int
    rate: Decimal
    confirmed: bool
    organization_id: int
    author_id: int
    manager_id: int
    client_id: int
    contract_id: int
    service_type_id: int

    class Config:
        from_attributes = True


class OrderRailWayInDB(OrderRailWayBase):
    id: int

    class Config:
        from_attributes = True