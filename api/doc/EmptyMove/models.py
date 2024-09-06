from sqlalchemy import Column, Integer, DateTime, String, ForeignKey, Numeric, Boolean
from sqlalchemy.orm import relationship
from config.db import Base
from sqlalchemy.sql import func


class EmptyMove(Base):
    __tablename__ = "empty_move"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime, default=func.now())


class EmptyMoveProvider(Base):
    __tablename__ = "empty_move_provider"

    id = Column(Integer, primary_key=True, index=True)
    empty_move_id = Column(Integer, ForeignKey('empty_move.id'), nullable=False)


class EmptyMoveShipment(Base):
    __tablename__ = "empty_move_shipment"

    id = Column(Integer, primary_key=True, index=True)
    empty_move_id = Column(Integer, ForeignKey('empty_move.id'), nullable=False)
