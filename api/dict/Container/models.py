from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from config.db import Base


# Класс - Вагон
class Container(Base):
    __tablename__ = "containers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(20), nullable=False)
    wagon_type_id = Column(Integer, ForeignKey('wagon_types.id'), default=0)
    wagon_type = relationship("WagonType", back_populates="containers")

    def __repr__(self):
        return f"'{self.name}'"
