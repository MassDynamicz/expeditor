from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from config.db import Base


class Subcode(Base):
    __tablename__ = "subcodes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)

    owner_id = Column(Integer, ForeignKey('rw_codes.id'), nullable=False)
    owner = relationship("RWCode", back_populates="subcodes")

    transport_subcode1 = relationship(
        "OrderRW_Transport",
        back_populates="subcode1",
        foreign_keys='OrderRW_Transport.subcode1_id'
    )

    transport_subcode2 = relationship(
        "OrderRW_Transport",
        back_populates="subcode2",
        foreign_keys='OrderRW_Transport.subcode2_id'
    )

    transport_subcode3 = relationship(
        "OrderRW_Transport",
        back_populates="subcode3",
        foreign_keys='OrderRW_Transport.subcode3_id'
    )

    transport_subcode4 = relationship(
        "OrderRW_Transport",
        back_populates="subcode4",
        foreign_keys='OrderRW_Transport.subcode4_id'
    )

    transport_subcode5 = relationship(
        "OrderRW_Transport",
        back_populates="subcode5",
        foreign_keys='OrderRW_Transport.subcode5_id'
    )

    def __repr__(self):
        return f"'{self.name}'"
