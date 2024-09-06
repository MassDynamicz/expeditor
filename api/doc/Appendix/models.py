from sqlalchemy import Column, Integer, DateTime, String, ForeignKey, Numeric, Boolean
from sqlalchemy.orm import relationship
from config.db import Base
from sqlalchemy.sql import func


class Appendix(Base):
    __tablename__ = "appendix"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime, default=func.now())
    comment = Column(String(300), default="")
    rate = Column(Numeric(15, 4), default=0)
    sum = Column(Numeric(15, 2), default=0)

    author_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    manager_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    organization_id = Column(Integer, ForeignKey('organizations.id'), nullable=False)
    client_id = Column(Integer, ForeignKey('contractors.id'), nullable=False)
    contract_id = Column(Integer, ForeignKey('contracts.id'), nullable=False)


class AppendixShipment(Base):
    __tablename__ = "appendix_shipments"

    id = Column(Integer, primary_key=True, index=True)
    appendix_id = Column(Integer, ForeignKey('appendix.id'), nullable=False)
    shipment_id = Column(Integer, ForeignKey('order_railway_shipment.id'), nullable=False)
