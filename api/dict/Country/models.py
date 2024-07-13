import enum
from sqlalchemy import Column, Integer, String, Boolean, Date, ForeignKey, Numeric, Enum
from sqlalchemy.orm import relationship
from config.db import Base


# Класс - Страна
class Country(Base):
    __tablename__ = "countries"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False)
    guid = Column(String(100), default="")
    full_name = Column(String(300), default="")
    code = Column(String(5), nullable=False)

    contractors = relationship("Contractor", back_populates="country")

    def __repr__(self):
        return f"'{self.name}'"
