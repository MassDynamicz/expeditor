from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from config.db import Base


# Класс - ЖД территории
class Territory(Base):
    __tablename__ = "territories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False)
    code = Column(String(10), nullable=False)

    stations = relationship("Station", back_populates="territory")
    rail_way_codes = relationship("RailWayCode", back_populates="territory")

    def __repr__(self):
        return f"'{self.name}'"
