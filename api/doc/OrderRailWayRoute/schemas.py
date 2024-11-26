from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from decimal import Decimal


class OrderRailWayRouteBase(BaseModel):
    index: int
    comment: Optional[str] = None
    weight: Decimal
    sum: Decimal
    amount: int
    price: Decimal
    sum: Decimal
    order_id: int
    station_otpr_id: int
    station_nazn_id: int
    wagon_type_id: int
    etsng_id: int
    gng_id: int
    vat_id: int

    class Config:
        from_attributes = True


class OrderRailWayRouteInDB(OrderRailWayRouteBase):
    id: int

    class Config:
        from_attributes = True
