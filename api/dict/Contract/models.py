from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from config.db import Base


# Класс - Договора
class Contract(Base):
    __tablename__ = "contracts"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False)
    guid = Column(String(100), nullable=True)
    number = Column(String(150), nullable=True)
    from_date = Column(Date, nullable=True)
    to_date = Column(Date, nullable=True)
    organization_id = Column(Integer, ForeignKey('organizations.id'), nullable=False)
    contractor_id = Column(Integer, ForeignKey('contractors.id'), nullable=False)
    currency_id = Column(Integer, ForeignKey('currencies.id'), nullable=False)

    def __repr__(self):
        return f"'{self.name}'"
