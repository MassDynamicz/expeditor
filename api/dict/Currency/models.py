from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from config.db import Base


# Класс - валюта
class Currency(Base):
    __tablename__ = "currencies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False)
    guid = Column(String(100), default="")
    code = Column(String(3), nullable=False)
    copybook_parameters_ru = Column(String(200), default="")
    copybook_parameters_en = Column(String(200), default="")

    bank_accounts = relationship("BankAccount", back_populates="currency")
    bank_accounts_org = relationship("BankAccountOrg", back_populates="currency")
    contracts = relationship("Contract", back_populates="currency")
    order_provider_currency = relationship("OrderRW_Provider", back_populates="currency")

    def __repr__(self):
        return f"'{self.name}'"
