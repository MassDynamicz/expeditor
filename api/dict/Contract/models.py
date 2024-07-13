from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from config.db import Base


# Класс - Договора
class Contract(Base):
    __tablename__ = "contracts"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False)
    guid = Column(String(100), default="")
    number = Column(String(150), default="")
    from_date = Column(Date)
    to_date = Column(Date)
    organization_id = Column(Integer, ForeignKey('organizations.id'), nullable=False)
    contractor_id = Column(Integer, ForeignKey('contractors.id'), nullable=False)
    currency_id = Column(Integer, ForeignKey('currencies.id'), nullable=False)

    organization = relationship("Organization", back_populates="contracts")
    contractor = relationship("Contractor", back_populates="contracts")
    currency = relationship("Currency", back_populates="contracts")
    orders_rw = relationship("OrderRW", back_populates="contract")
    order_provider_contract = relationship("OrderRW_Provider", back_populates="contract")

    def __repr__(self):
        return f"'{self.name}'"
