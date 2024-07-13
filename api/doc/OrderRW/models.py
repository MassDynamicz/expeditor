from sqlalchemy import Column, Integer, DateTime, String, Boolean, Date, ForeignKey, Numeric
from sqlalchemy.orm import relationship
from config.db import Base
from sqlalchemy.sql import func


class OrderRW(Base):
    __tablename__ = "order_rw"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime, default=func.now())
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    comment = Column(String(300), default="")
    sum = Column(Numeric(15, 2), default=0)
    amount = Column(Integer, default=0)
    rate = Column(Numeric(15, 4), default=0)

    organization_id = Column(Integer, ForeignKey('organizations.id'), nullable=False)
    organization = relationship("Organization", back_populates="orders_rw")

    # author_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    # author = relationship("User", back_populates="orders_rw_author", foreign_keys=[author_id])

    # manager_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    # manager = relationship("User", back_populates="orders_rw_manager", foreign_keys=[manager_id])

    client_id = Column(Integer, ForeignKey('contractors.id'), nullable=False)
    client = relationship("Contractor", back_populates="orders_rw")

    contract_id = Column(Integer, ForeignKey('contracts.id'), nullable=False)
    contract = relationship("Contract", back_populates="orders_rw")

    service_type_id = Column(Integer, ForeignKey('service_types.id'), nullable=False)
    service_type = relationship("ServiceType", back_populates="orders_rw")
