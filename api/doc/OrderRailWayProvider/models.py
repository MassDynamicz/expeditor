from sqlalchemy import Column, Integer, DateTime, String, ForeignKey, Numeric, Boolean
from sqlalchemy.orm import relationship
from config.db import Base
from sqlalchemy.sql import func


class OrderRailWayProvider(Base):
    __tablename__ = "order_railway_provider"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    rate = Column(Numeric(15, 4), default=0)
    sum_plan = Column(Numeric(15, 2), default=0)
    sum_fact = Column(Numeric(15, 2), default=0)

    shipment_id = Column(Integer, ForeignKey('order_railway_shipment.id'), nullable=False)
    provider_id = Column(Integer, ForeignKey('contractors.id'), nullable=False)
    contract_id = Column(Integer, ForeignKey('contracts.id'), nullable=False)
    operation_id = Column(Integer, ForeignKey('operations.id'), nullable=False)
    vat_id = Column(Integer, ForeignKey('vat.id'), nullable=False)
    # invoice_id = Column(Integer, ForeignKey('invoices.id'), nullable=True)
    # expense_registration_id = Column(Integer, ForeignKey('expense_registrations.id'), nullable=True)
