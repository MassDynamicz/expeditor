from sqlalchemy import Column, Integer, String, ForeignKey, Numeric, Date
from sqlalchemy.orm import relationship
from config.db import Base


class ActOut(Base):
    __tablename__ = "act_out"

    id = Column(Integer, primary_key=True, index=True)
    guid = Column(String(100), nullable=True)
    number = Column(String(30), nullable=False)
    date = Column(Date)
    operation_type = Column(String(150), nullable=False)
    rate = Column(Numeric(15, 4), default=0)
    sum = Column(Numeric(15, 2), default=0)
    comment = Column(String(300), default="")

    organization_id = Column(Integer, ForeignKey('organizations.id'), nullable=False)
    contractor_id = Column(Integer, ForeignKey('contractors.id'), nullable=False)
    contract_id = Column(Integer, ForeignKey('contracts.id'), nullable=False)

    contractor = relationship("Contractor", backref="acts_out_contractors")
    contract = relationship("Contract", backref="acts_out_contracts")
    organization = relationship("Organization", backref="acts_out_organizations")
