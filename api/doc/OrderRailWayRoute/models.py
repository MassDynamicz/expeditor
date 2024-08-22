from sqlalchemy import Column, Integer, DateTime, String, ForeignKey, Numeric
from sqlalchemy.orm import relationship
from config.db import Base
from sqlalchemy.sql import func


class OrderRailWayRoute(Base):
    __tablename__ = "order_railway_route"

    id = Column(Integer, primary_key=True, index=True)
    index = Column(Integer, default=0)
    date = Column(DateTime, default=func.now())
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    comment = Column(String(300), default="")
    weight = Column(Numeric(15, 4), default=0)
    amount = Column(Integer, default=0)
    price = Column(Numeric(15, 2), default=0)
    sum = Column(Numeric(15, 2), default=0)
    order_id = Column(Integer, ForeignKey('order_railway.id'), nullable=False)
    station_otpr_id = Column(Integer, ForeignKey('stations.id'), nullable=False)
    station_nazn_id = Column(Integer, ForeignKey('stations.id'), nullable=False)
    wagon_type_id = Column(Integer, ForeignKey('wagon_types.id'), nullable=False)
    etsng_id = Column(Integer, ForeignKey('etsng.id'), nullable=True)
    gng_id = Column(Integer, ForeignKey('gng.id'), nullable=True)
    vat_id = Column(Integer, ForeignKey('vat.id'), nullable=False)

    order = relationship("OrderRailWay", backref="order_railway_routes")
    station_otpr = relationship("Station", foreign_keys=[station_otpr_id], backref="order_railway_routes_stations_otpr")
    station_nazn = relationship("Station", foreign_keys=[station_nazn_id], backref="order_railway_routes_stations_nazn")
    wagon_type = relationship("WagonType", backref="order_railway_routes")
    etsng = relationship("Etsng", backref="order_railway_routes")
    gng = relationship("Gng", backref="order_railway_routes")
    vat = relationship("Vat", backref="order_railway_routes")
