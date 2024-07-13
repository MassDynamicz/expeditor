from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from config.db import Base


# Класс - Банковские счета организации
class BankAccountOrg(Base):
    __tablename__ = "bank_accounts_org"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False)
    guid = Column(String(100), default="")
    number = Column(String(150), default="")
    currency_id = Column(Integer, ForeignKey('currencies.id'), nullable=False)
    bank_id = Column(Integer, ForeignKey('banks.id'), nullable=False)
    owner_id = Column(Integer, ForeignKey('organizations.id'), nullable=False)

    currency = relationship("Currency", back_populates="bank_accounts_org")
    bank = relationship("Bank", back_populates="bank_accounts_org")
    owner = relationship("Organization", back_populates="bank_accounts_org")

    def __repr__(self):
        return f"'{self.name}'"
