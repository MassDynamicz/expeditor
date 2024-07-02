import enum
from sqlalchemy import Column, Integer, String, Boolean, Date, ForeignKey, Numeric, Enum
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

    def __repr__(self):
        return f"'{self.name}'"
