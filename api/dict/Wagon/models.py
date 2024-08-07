from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from config.db import Base



# Класс - Вагон
class Wagon(Base):
    __tablename__ = "wagons"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(20), nullable=False)
    wagon_type_id = Column(Integer, ForeignKey('wagon_types.id'), default=None)
    wagon_type = relationship("WagonType", back_populates="wagons")

    dislocation_wagon = relationship("Dislocation", back_populates="wagon")

    def __repr__(self):
        return f"'{self.name}'"
