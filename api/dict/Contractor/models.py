from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Enum
from sqlalchemy.orm import relationship
from api.dict.OwnerType.models import OwnerType
from config.db import Base


# Класс - Контрагент
class Contractor(Base):
    __tablename__ = "contractors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False)
    guid = Column(String(100), nullable=True)
    full_name = Column(String(300), nullable=True)
    bin = Column(String(15), nullable=True)
    kbe = Column(String(10), nullable=True)
    enterpreneur = Column(Boolean, default=False)
    legal_address = Column(String(300), nullable=True)
    comment = Column(String(300), nullable=True)
    document = Column(String(300), nullable=True)
    owner_type = Column(Enum(OwnerType), nullable=False)
    country_id = Column(Integer, ForeignKey('countries.id'), nullable=True)

    def __repr__(self):
        return f"'{self.name}'"
