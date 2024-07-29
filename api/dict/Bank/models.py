from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from config.db import Base


# Класс - Банк
class Bank(Base):
    __tablename__ = "banks"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False)
    guid = Column(String(100), nullable=True)
    bik = Column(String(50), nullable=True)
    city = Column(String(100), nullable=True)

    def __repr__(self):
        return f"'{self.name}'"
