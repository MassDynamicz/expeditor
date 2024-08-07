from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from config.db import Base


# Класс - Виды услуг
class RailWayCode(Base):
    __tablename__ = "rail_way_codes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    code = Column(String(20), nullable=False)

    owner_id = Column(Integer, ForeignKey('contractors.id'), nullable=False)
    owner = relationship("Contractor", back_populates="rail_way_codes")

    territory_id = Column(Integer, ForeignKey('territories.id'), nullable=False)
    territory = relationship("Territory", back_populates="rail_way_codes")

    subcodes = relationship("Subcode", back_populates="owner")

    def __repr__(self):
        return f"'{self.name}'"
