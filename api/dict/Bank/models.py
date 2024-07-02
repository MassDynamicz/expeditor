from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from config.db import Base


# Класс - Банк
class Bank(Base):
    __tablename__ = "banks"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False)
    guid = Column(String(100), default="")
    bik = Column(String(50), default="")
    city = Column(String(100), default="")

    bank_accounts = relationship("BankAccount", back_populates="bank")
    bank_accounts_org = relationship("BankAccountOrg", back_populates="bank")

    def __repr__(self):
        return f"'{self.name}'"
