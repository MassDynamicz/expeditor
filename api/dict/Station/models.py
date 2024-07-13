from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from config.db import Base


# Класс - ЖД станции
class Station(Base):
    __tablename__ = "stations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False)
    code = Column(String(20), unique=True, nullable=False)
    territory_id = Column(Integer, ForeignKey('territories.id'), nullable=False)
    territory = relationship("Territory", back_populates="stations")
    latitude = Column(String(100), default='')
    longitude = Column(String(100), default='')

    dislocation_station_otpr = relationship(
        "Dislocation",
        back_populates="station_otpr",
        foreign_keys='Dislocation.station_otpr_id'
    )

    dislocation_station_tek = relationship(
        "Dislocation",
        back_populates="station_tek",
        foreign_keys='Dislocation.station_tek_id'
    )

    dislocation_station_nazn = relationship(
        "Dislocation",
        back_populates="station_nazn",
        foreign_keys='Dislocation.station_nazn_id'
    )

    orderrw_station_otpr = relationship(
        "OrderRW_Route",
        back_populates="station_otpr",
        foreign_keys='OrderRW_Route.station_otpr_id'
    )

    orderrw_station_nazn = relationship(
        "OrderRW_Route",
        back_populates="station_nazn",
        foreign_keys='OrderRW_Route.station_nazn_id'
    )

    transport_station_otpr = relationship(
        "OrderRW_Transport",
        back_populates="station_otpr",
        foreign_keys='OrderRW_Transport.station_otpr_id'
    )

    transport_station_nazn = relationship(
        "OrderRW_Transport",
        back_populates="station_nazn",
        foreign_keys='OrderRW_Transport.station_nazn_id'
    )

    def __repr__(self):
        return f"'{self.name}'"
