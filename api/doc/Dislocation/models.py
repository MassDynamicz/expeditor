from sqlalchemy import Column, Integer, DateTime, String, ForeignKey, Numeric, Boolean, Date
from sqlalchemy.orm import relationship
from config.db import Base
from sqlalchemy.sql import func


class Dislocation(Base):
    __tablename__ = "dislocation"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime, default=func.now())
    loaded = Column(Boolean, default=False)
    nomer_nakladnoi = Column(String(30), nullable=True)
    date_otpr = Column(Date)
    date_otpr_time = Column(DateTime)
    date_oper = Column(Date)
    date_arrive = Column(Date, nullable=True)
    date_arrive_plan = Column(Date, nullable=True)
    operation = Column(String(300), nullable=True)
    operation_id = Column(String(300), nullable=True)
    operation_code = Column(String(300), nullable=True)
    broken = Column(Boolean, default=False)
    weight = Column(Numeric(15, 4), default=0)
    distance_end = Column(Integer, default=0)
    distance_full = Column(Integer, default=0)
    group_name = Column(String(50), nullable=True)
    group_id = Column(String(50), nullable=True)
    gruz_sender = Column(String(200), nullable=True)
    gruz_receiver = Column(String(200), nullable=True)
    payer = Column(String(200), nullable=True)
    owner = Column(String(200), nullable=True)
    owner_code = Column(String(200), nullable=True)
    next_repair = Column(Date, nullable=True)
    next_repair_type = Column(String(200), nullable=True)
    days_wo_movement = Column(Numeric(15, 2), default=0)
    days_wo_operation = Column(Numeric(15, 2), default=0)
    days_in_transit = Column(Numeric(15, 2), default=0)
    vagon_comment = Column(String(200), nullable=True)

    flight_id = Column(Integer, ForeignKey('flights.id'), nullable=True)
    flight = relationship("Flight", backref="dislocation_flight")

    wagon_id = Column(Integer, ForeignKey('wagons.id'), nullable=True)
    wagon = relationship("Wagon", backref="dislocation_wagon")

    container_id = Column(Integer, ForeignKey('containers.id'), nullable=True)
    container = relationship("Container", backref="dislocation_container")

    station_otpr_id = Column(Integer, ForeignKey('stations.id'), nullable=True)
    station_otpr = relationship("Station", backref="dislocation_station_otpr", foreign_keys=[station_otpr_id])

    station_tek_id = Column(Integer, ForeignKey('stations.id'), nullable=True)
    station_tek = relationship("Station", backref="dislocation_station_tek", foreign_keys=[station_tek_id])

    station_nazn_id = Column(Integer, ForeignKey('stations.id'), nullable=True)
    station_nazn = relationship("Station", backref="dislocation_station_nazn", foreign_keys=[station_nazn_id])

    etsng_id = Column(Integer, ForeignKey('etsng.id'), nullable=True)
    etsng = relationship("Etsng", backref="dislocation_etsng", foreign_keys=[etsng_id])

    prev_etsng_id = Column(Integer, ForeignKey('etsng.id'), nullable=True)
    prev_etsng = relationship("Etsng", backref="dislocation_prev_etsng", foreign_keys=[prev_etsng_id])
