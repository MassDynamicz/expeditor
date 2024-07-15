import enum
from sqlalchemy import Column, Integer, String, Boolean, Date, ForeignKey, Numeric, Enum
from sqlalchemy.orm import relationship
from api.dict.OwnerType.models import OwnerType
from config.db import Base


# Класс - Организация
class Organization(Base):
    __tablename__ = "organizations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False)
    guid = Column(String(100), default="")
    full_name = Column(String(300), default="")
    bin = Column(String(15), nullable=False)
    kbe = Column(String(10), default="")
    enterpreneur = Column(Boolean, default=False)
    legal_address = Column(String(300), default="")
    owner_type = Column(Enum(OwnerType), nullable=False)
    country_id = Column(Integer, ForeignKey('countries.id'), nullable=True)

    # Определяем отношение
    country = relationship("Country", lazy='joined')
    contracts = relationship("Contract", back_populates="organization")
    bank_accounts_org = relationship("BankAccountOrg", back_populates="owner")

    def __repr__(self):
        return f"'{self.name}'"
