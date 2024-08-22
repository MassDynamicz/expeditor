from sqlalchemy import Column, Integer, DateTime, String, ForeignKey, Numeric, Boolean
from sqlalchemy.orm import relationship
from config.db import Base
from sqlalchemy.sql import func


class OrderRailWay(Base):
    __tablename__ = "order_railway"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime, default=func.now())
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    number = Column(String(50), default="")
    comment = Column(String(300), default="")
    sum = Column(Numeric(15, 2), default=0)
    amount = Column(Integer, default=0)
    rate = Column(Numeric(15, 4), default=0)
    confirmed = Column(Boolean, default=False)
    organization_id = Column(Integer, ForeignKey('organizations.id'), nullable=False)
    author_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    manager_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    client_id = Column(Integer, ForeignKey('contractors.id'), nullable=False)
    contract_id = Column(Integer, ForeignKey('contracts.id'), nullable=False)
    service_type_id = Column(Integer, ForeignKey('service_types.id'), nullable=False)

    organization = relationship("Organization", backref="orders_rail_way")
    author = relationship("User", foreign_keys=[author_id], backref="orders_rail_way_author")
    manager = relationship("User", foreign_keys=[manager_id], backref="orders_rail_way_manager")
    client = relationship("Contractor", backref="orders_rail_way")
    contract = relationship("Contract", backref="orders_rail_way")
    service_type = relationship("ServiceType", backref="orders_rail_way")
