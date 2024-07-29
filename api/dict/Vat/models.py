from sqlalchemy import Column, Integer, String, Numeric
from sqlalchemy.orm import relationship
from config.db import Base


# Класс - ставка НДС
class Vat(Base):
    __tablename__ = "vat"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False)
    guid = Column(String(100), nullable=True)
    rate = Column(Numeric(15, 4), default=0)

    def __repr__(self):
        return f"'{self.name}'"
