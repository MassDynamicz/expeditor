from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from config.db import Base


class Subcode(Base):
    __tablename__ = "subcodes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)

    owner_id = Column(Integer, ForeignKey('rail_way_codes.id'), nullable=False)
    owner = relationship("RailWayCode", back_populates="subcodes")

    def __repr__(self):
        return f"'{self.name}'"
