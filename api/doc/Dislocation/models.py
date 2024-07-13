from sqlalchemy import Column, Integer, DateTime, String, Boolean, Date, ForeignKey, Numeric
from sqlalchemy.orm import relationship
from config.db import Base
from sqlalchemy.sql import func


# Класс - Дислокация вагонов и контейнеров
class Dislocation(Base):
    __tablename__ = "dislocation"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime, default=func.now())
    loaded = Column(Boolean, default=False)
    nomer_nakladnoi = Column(String(30), default="")
    date_otpr = Column(Date)
    date_otpr_time = Column(DateTime)
    date_oper = Column(Date)
    date_arrive = Column(Date, nullable=True)
    date_arrive_plan = Column(Date, nullable=True)
    operation = Column(String(300), default="")
    operation_id = Column(String(300), default="")
    operation_code = Column(String(300), default="")
    broken = Column(Boolean, default=False)
    weight = Column(Numeric(15, 4), default=0)
    distance_end = Column(Integer, default=0)
    distance_full = Column(Integer, default=0)
    group_name = Column(String(50), default="")
    group_id = Column(String(50), default="")
    gruz_sender = Column(String(200), default="")
    gruz_receiver = Column(String(200), default="")
    payer = Column(String(200), default="")
    owner = Column(String(200), default="")
    owner_code = Column(String(200), default="")
    next_repair = Column(Date, nullable=True)
    next_repair_type = Column(String(200), default="")
    days_wo_movement = Column(Numeric(15, 2), default=0)
    days_wo_operation = Column(Numeric(15, 2), default=0)
    days_in_transit = Column(Numeric(15, 2), default=0)
    vagon_comment = Column(String(200), default="")

    wagon_id = Column(Integer, ForeignKey('wagons.id'), nullable=True)
    wagon = relationship("Wagon", back_populates="dislocation_wagon")

    container_id = Column(Integer, ForeignKey('containers.id'), nullable=True)
    container = relationship("Container", back_populates="dislocation_container")

    station_otpr_id = Column(Integer, ForeignKey('stations.id'), nullable=True)
    station_otpr = relationship("Station", back_populates="dislocation_station_otpr", foreign_keys=[station_otpr_id])

    station_tek_id = Column(Integer, ForeignKey('stations.id'), nullable=True)
    station_tek = relationship("Station", back_populates="dislocation_station_tek", foreign_keys=[station_tek_id])

    station_nazn_id = Column(Integer, ForeignKey('stations.id'), nullable=True)
    station_nazn = relationship("Station", back_populates="dislocation_station_nazn", foreign_keys=[station_nazn_id])

    etsng_id = Column(Integer, ForeignKey('etsng.id'), nullable=True)
    etsng = relationship("Etsng", back_populates="dislocation_etsng", foreign_keys=[etsng_id])

    prev_etsng_id = Column(Integer, ForeignKey('etsng.id'), nullable=True)
    prev_etsng = relationship("Etsng", back_populates="dislocation_prev_etsng", foreign_keys=[prev_etsng_id])
