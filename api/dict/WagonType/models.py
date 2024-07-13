from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from config.db import Base


# Класс - Роды подвижного состава
class WagonType(Base):
    __tablename__ = "wagon_types"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False)
    code = Column(String(20), unique=True, nullable=False)
    official_name = Column(String(300), default='')
    key_names = Column(String(500), default='')
    platform = Column(Boolean, default=False)

    wagons = relationship("Wagon", back_populates="wagon_type")
    containers = relationship("Container", back_populates="wagon_type")
    orderrw_routes = relationship("OrderRW_Route", back_populates="wagon_type")
    transport_wagon_type = relationship("OrderRW_Transport", back_populates="wagon_type")

    def __repr__(self):
        return f"'{self.name}'"
