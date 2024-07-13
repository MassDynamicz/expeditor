import enum
from sqlalchemy import Column, Integer, String, Boolean, Date, ForeignKey, Numeric, Enum
from sqlalchemy.orm import relationship
from config.db import Base


# Класс - ЕТСНГ
class Etsng(Base):
    __tablename__ = "etsng"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    code = Column(String(20), unique=True, nullable=False)

    dislocation_etsng = relationship("Dislocation", back_populates="etsng",
                                           foreign_keys='Dislocation.etsng_id')
    dislocation_prev_etsng = relationship("Dislocation", back_populates="prev_etsng",
                                            foreign_keys='Dislocation.prev_etsng_id')
    orderrw_routes = relationship("OrderRW_Route", back_populates="etsng")
    transport_etsng = relationship("OrderRW_Transport", back_populates="etsng")

    def __repr__(self):
        return f"'{self.name}'"
