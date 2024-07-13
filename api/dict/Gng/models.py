from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from config.db import Base


# Класс - ГНГ
class Gng(Base):
    __tablename__ = "gng"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(300), nullable=False)
    code = Column(String(20), unique=True, nullable=False)
    code_etsng = Column(String(20), nullable=True)

    orderrw_routes = relationship("OrderRW_Route", back_populates="gng")
    transport_gng = relationship("OrderRW_Transport", back_populates="gng")

    def __repr__(self):
        return f"'{self.name}'"
