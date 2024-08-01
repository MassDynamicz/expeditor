from sqlalchemy import Column, Integer, DateTime, String, ForeignKey, Numeric, Boolean
from sqlalchemy.orm import relationship
from config.db import Base
from sqlalchemy.sql import func


class OrderRailWay(Base):
    __tablename__ = "order_railway"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime, default=func.now())  #editable
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    comment = Column(String(300), default="")  #editable
    sum = Column(Numeric(15, 2), default=0)  #calcuted
    amount = Column(Integer, default=0)  #calcuted
    rate = Column(Numeric(15, 4), default=0)  #calcuted #editable
    confirmed = Column(Boolean, default=False)  #editable
    organization_id = Column(Integer, ForeignKey('organizations.id'), nullable=False)  #deafult #editable
    author_id = Column(Integer, ForeignKey('users.id'), nullable=False)  #default
    manager_id = Column(Integer, ForeignKey('users.id'), nullable=False)  #deafault #editable
    client_id = Column(Integer, ForeignKey('contractors.id'), nullable=False)  #editable
    contract_id = Column(Integer, ForeignKey('contracts.id'), nullable=False)  #editable
    service_type_id = Column(Integer, ForeignKey('service_types.id'), nullable=False)  #editable
