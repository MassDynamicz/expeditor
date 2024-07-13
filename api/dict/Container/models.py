from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from config.db import Base


# Класс - Вагон
class Container(Base):
    __tablename__ = "containers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(20), nullable=False)
    wagon_type_id = Column(Integer, ForeignKey('wagon_types.id'), default=None)
    wagon_type = relationship("WagonType", back_populates="containers")

    dislocation_container = relationship("Dislocation", back_populates="container")
    transport_containers = relationship("OrderRW_Transport", back_populates="container")

    def __repr__(self):
        return f"'{self.name}'"
