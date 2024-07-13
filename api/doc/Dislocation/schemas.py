from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime
from decimal import Decimal


class DislocationBase(BaseModel):
    id: int
    date: datetime
    loaded: bool
    nomer_nakladnoi: Optional[str] = ""
    date_otpr: Optional[date] = None
    date_otpr_time: Optional[datetime] = None
    date_oper: Optional[date] = None
    date_arrive: Optional[date] = None
    date_arrive_plan: Optional[date] = None
    operation: Optional[str] = ""
    operation_id: Optional[str] = ""
    operation_code: Optional[str] = ""
    broken: bool
    weight: Decimal
    distance_end: Optional[int] = 0
    distance_full: Optional[int] = 0
    group_name: Optional[str] = ""
    group_id: Optional[str] = ""
    gruz_sender: Optional[str] = ""
    gruz_receiver: Optional[str] = ""
    payer: Optional[str] = ""
    owner: Optional[str] = ""
    owner_code: Optional[str] = ""
    next_repair: Optional[date] = None
    next_repair_type: Optional[str] = ""
    days_wo_movement: Decimal
    days_wo_operation: Decimal
    days_in_transit: Decimal
    vagon_comment: Optional[str] = ""
    wagon_id: Optional[int] = None
    container_id: Optional[int] = None
    station_otpr_id: Optional[int] = None
    station_tek_id: Optional[int] = None
    station_nazn_id: Optional[int] = None
    etsng_id: Optional[int] = None
    prev_etsng_id: Optional[int] = None

    class Config:
        from_attributes = True
