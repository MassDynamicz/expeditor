from sqlalchemy import Column, Integer, DateTime, String, ForeignKey, Numeric, Boolean
from sqlalchemy.orm import relationship
from config.db import Base
from sqlalchemy.sql import func


class OrderRailWayShipment(Base):
    __tablename__ = "order_railway_shipment"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    weight = Column(Numeric(15, 4), default=0)
    date_departure = Column(DateTime, nullable=True)
    date_departure_sng = Column(DateTime, nullable=True)
    date_reload = Column(DateTime, nullable=True)
    date_arrival = Column(DateTime, nullable=True)
    date_arrival_border = Column(DateTime, nullable=True)
    profit = Column(Numeric(15, 2), default=0)
    comment = Column(String(300), default="")
    rate = Column(Numeric(15, 4), default=0)
    nomer_nakladnoi = Column(String(50), nullable=True)
    sum = Column(Numeric(15, 2), default=0)

    order_id = Column(Integer, ForeignKey('order_railway.id'), nullable=False)
    wagon_id = Column(Integer, ForeignKey('wagons.id'), nullable=True)
    wagon2_id = Column(Integer, ForeignKey('wagons.id'), nullable=True)
    gng_id = Column(Integer, ForeignKey('gng.id'), nullable=True)
    etsng_id = Column(Integer, ForeignKey('etsng.id'), nullable=True)
    container_id = Column(Integer, ForeignKey('containers.id'), nullable=True)
    wagon_type_id = Column(Integer, ForeignKey('wagon_types.id'), nullable=False)
    vat_id = Column(Integer, ForeignKey('vat.id'), nullable=False)
    station_otpr_id = Column(Integer, ForeignKey('stations.id'), nullable=False)
    station_nazn_id = Column(Integer, ForeignKey('stations.id'), nullable=False)
