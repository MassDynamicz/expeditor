from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Date
from sqlalchemy.orm import relationship
from config.db import Base


class Flight(Base):
    __tablename__ = "flights"

    id = Column(Integer, primary_key=True, index=True)
    loaded = Column(Boolean, default=False)
    nomer_nakladnoi = Column(String(30), nullable=True)
    date_otpr = Column(Date)
    date_arrive = Column(Date, nullable=True)

    wagon_id = Column(Integer, ForeignKey('wagons.id'), nullable=True)
    wagon = relationship("Wagon", backref="flight_wagon")

    station_otpr_id = Column(Integer, ForeignKey('stations.id'), nullable=True)
    station_otpr = relationship("Station", backref="flight_station_otpr", foreign_keys=[station_otpr_id])

    station_nazn_id = Column(Integer, ForeignKey('stations.id'), nullable=True)
    station_nazn = relationship("Station", backref="flight_station_nazn", foreign_keys=[station_nazn_id])


class FlightContainers(Base):
    __tablename__ = "flights_containers"

    id = Column(Integer, primary_key=True, index=True)
    container_id = Column(Integer, ForeignKey('containers.id'), nullable=True)
    container = relationship("Container", backref="flight_containers")
