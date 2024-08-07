import enum
from sqlalchemy import Column, Integer, String, Boolean, Date, ForeignKey, Numeric, Enum
from sqlalchemy.orm import relationship
from config.db import Base


# Класс - Операции
class Operation(Base):
    __tablename__ = "operations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    code = Column(String(20), default='')
    vat_id = Column(Integer, ForeignKey('vat.id'), default=0)
    vat = relationship("Vat", back_populates="operations")

    def __repr__(self):
        return f"'{self.name}'"
