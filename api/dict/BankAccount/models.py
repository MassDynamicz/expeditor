from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from config.db import Base


# Класс - Банковские счета контрагентов
class BankAccount(Base):
    __tablename__ = "bank_accounts"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False)
    guid = Column(String(100), nullable=True)
    number = Column(String(150), nullable=False)
    currency_id = Column(Integer, ForeignKey('currencies.id'), nullable=False)
    bank_id = Column(Integer, ForeignKey('banks.id'), nullable=False)
    contractor_id = Column(Integer, ForeignKey('contractors.id'), nullable=True)
    organization_id = Column(Integer, ForeignKey('organizations.id'), nullable=True)

    bank = relationship("Bank", backref="bank_accounts")
    currency = relationship("Currency", backref="bank_accounts")
    contractor = relationship("Contractor", backref="bank_accounts")
    organization = relationship("Organization", backref="bank_accounts")

    def __repr__(self):
        return f"'{self.name}'"
