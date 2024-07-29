from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from config.db import Base


# Класс - валюта
class Currency(Base):
    __tablename__ = "currencies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False)
    guid = Column(String(100), nullable=True)
    code = Column(String(3), nullable=False)
    copybook_parameters_ru = Column(String(200), nullable=True)
    copybook_parameters_en = Column(String(200), nullable=True)

    def __repr__(self):
        return f"'{self.name}'"
