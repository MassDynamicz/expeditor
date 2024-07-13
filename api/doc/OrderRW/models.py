from sqlalchemy import Column, Integer, Date, DateTime, String, ForeignKey, Numeric, Boolean
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
    confirmed = Column(Boolean, default=False)

    organization_id = Column(Integer, ForeignKey('organizations.id'), nullable=False)
    organization = relationship("Organization", back_populates="orders_rw")

    author_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    author = relationship("User", back_populates="orders_rw_author", foreign_keys=[author_id])

    manager_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    manager = relationship("User", back_populates="orders_rw_manager", foreign_keys=[manager_id])

    client_id = Column(Integer, ForeignKey('contractors.id'), nullable=False)
    client = relationship("Contractor", back_populates="orders_rw")

    contract_id = Column(Integer, ForeignKey('contracts.id'), nullable=False)
    contract = relationship("Contract", back_populates="orders_rw")

    service_type_id = Column(Integer, ForeignKey('service_types.id'), nullable=False)
    service_type = relationship("ServiceType", back_populates="orders_rw")

    orderrw_routes = relationship("OrderRW_Route", back_populates="orderrw")
    orderrw_transport = relationship("OrderRW_Transport", back_populates="orderrw")


class OrderRW_Route(Base):
    __tablename__ = "order_rw_route"
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    weight = Column(Numeric(15, 4), default=0)
    amount = Column(Integer, default=0)
    price = Column(Numeric(15, 2), default=0)
    sum = Column(Numeric(15, 2), default=0)
    comment = Column(String(300), default="")

    orderrw_id = Column(Integer, ForeignKey('order_rw.id'), nullable=False)
    orderrw = relationship("OrderRW", back_populates="orderrw_routes")

    station_otpr_id = Column(Integer, ForeignKey('stations.id'), nullable=False)
    station_otpr = relationship("Station", back_populates="orderrw_station_otpr", foreign_keys=[station_otpr_id])

    station_nazn_id = Column(Integer, ForeignKey('stations.id'), nullable=False)
    station_nazn = relationship("Station", back_populates="orderrw_station_nazn", foreign_keys=[station_nazn_id])

    wagon_type_id = Column(Integer, ForeignKey('wagon_types.id'), nullable=False)
    wagon_type = relationship("WagonType", back_populates="orderrw_routes")

    etsng_id = Column(Integer, ForeignKey('etsng.id'), nullable=True)
    etsng = relationship("Etsng", back_populates="orderrw_routes")

    gng_id = Column(Integer, ForeignKey('gng.id'), nullable=True)
    gng = relationship("Gng", back_populates="orderrw_routes")

    vat_id = Column(Integer, ForeignKey('vat.id'), nullable=False)
    vat = relationship("Vat", back_populates="orderrw_routes")


class OrderRW_Transport(Base):
    __tablename__ = "order_rw_transport"
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    date_otpr = Column(Date, nullable=True)
    date_otpr_sng = Column(Date, nullable=True)
    date_transshipment = Column(Date, nullable=True)
    date_arrive = Column(Date, nullable=True)
    date_arrive_border = Column(Date, nullable=True)
    profit = Column(Numeric(15, 2), default=0)
    comment = Column(String(300), default="")
    td = Column(String(300), default="")
    rate = Column(Numeric(15, 4), default=0)
    otpr_number = Column(String(100), default="")
    sum = Column(Numeric(15, 2), default=0)
    weight = Column(Numeric(15, 4), default=0)

    orderrw_id = Column(Integer, ForeignKey('order_rw.id'), nullable=False)
    orderrw = relationship("OrderRW", back_populates="orderrw_transport")

    station_otpr_id = Column(Integer, ForeignKey('stations.id'), nullable=False)
    station_otpr = relationship("Station", back_populates="transport_station_otpr", foreign_keys=[station_otpr_id])

    station_nazn_id = Column(Integer, ForeignKey('stations.id'), nullable=False)
    station_nazn = relationship("Station", back_populates="transport_station_nazn", foreign_keys=[station_nazn_id])

    wagon_id = Column(Integer, ForeignKey('wagons.id'), nullable=True)
    wagon = relationship("Wagon", back_populates="transport_wagons", foreign_keys=[wagon_id])

    wagon_cn_id = Column(Integer, ForeignKey('wagons.id'), nullable=True)
    wagon_cn = relationship("Wagon", back_populates="transport_wagons_cn", foreign_keys=[wagon_cn_id])

    container_id = Column(Integer, ForeignKey('containers.id'), nullable=True)
    container = relationship("Container", back_populates="transport_containers")

    subcode1_id = Column(Integer, ForeignKey('subcodes.id'), nullable=True)
    subcode1 = relationship("Subcode", back_populates="transport_subcode1", foreign_keys=[subcode1_id])

    subcode2_id = Column(Integer, ForeignKey('subcodes.id'), nullable=True)
    subcode2 = relationship("Subcode", back_populates="transport_subcode2", foreign_keys=[subcode2_id])

    subcode3_id = Column(Integer, ForeignKey('subcodes.id'), nullable=True)
    subcode3 = relationship("Subcode", back_populates="transport_subcode3", foreign_keys=[subcode3_id])

    subcode4_id = Column(Integer, ForeignKey('subcodes.id'), nullable=True)
    subcode4 = relationship("Subcode", back_populates="transport_subcode4", foreign_keys=[subcode4_id])

    subcode5_id = Column(Integer, ForeignKey('subcodes.id'), nullable=True)
    subcode5 = relationship("Subcode", back_populates="transport_subcode5", foreign_keys=[subcode5_id])

    etsng_id = Column(Integer, ForeignKey('etsng.id'), nullable=True)
    etsng = relationship("Etsng", back_populates="transport_etsng")

    gng_id = Column(Integer, ForeignKey('gng.id'), nullable=True)
    gng = relationship("Gng", back_populates="transport_gng")

    wagon_type_id = Column(Integer, ForeignKey('wagon_types.id'), nullable=False)
    wagon_type = relationship("WagonType", back_populates="transport_wagon_type")

    vat_id = Column(Integer, ForeignKey('vat.id'), nullable=False)
    vat = relationship("Vat", back_populates="transport_vat")


class OrderRW_Provider(Base):
    __tablename__ = "order_rw_provider"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    rate = Column(Numeric(15, 4), default=0)
    sum_plan = Column(Numeric(15, 4), default=0)
    sum_fact = Column(Numeric(15, 4), default=0)
    card_number = Column(String(100), default="")
    scroll = Column(String(100), default="")

    provider_id = Column(Integer, ForeignKey('contractors.id'), nullable=False)
    provider = relationship("Contractor", back_populates="order_provider_provider")

    contract_id = Column(Integer, ForeignKey('contracts.id'), nullable=False)
    contract = relationship("Contract", back_populates="order_provider_contract")

    currency_id = Column(Integer, ForeignKey('currencies.id'), nullable=False)
    currency = relationship("Currency", back_populates="order_provider_currency")

    operation_id = Column(Integer, ForeignKey('operations.id'), nullable=False)
    operation = relationship("Operation", back_populates="order_provider_operation")

    vat_id = Column(Integer, ForeignKey('vat.id'), nullable=False)
    vat = relationship("Vat", back_populates="order_provider_vat")
