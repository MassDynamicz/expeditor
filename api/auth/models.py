from sqlalchemy import (
    Column, Integer, String, Boolean, DateTime, ForeignKey, BigInteger
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from config.db import Base
from config.utils import format_date


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    first_name = Column(String(50), nullable=True)
    last_name = Column(String(50), nullable=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    phone = Column(String(20), nullable=True)
    address = Column(String(255), nullable=True)
    company = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False, onupdate=func.now())
    role_id = Column(Integer, ForeignKey('roles.id'), nullable=True)
    role = relationship("Role", back_populates="users")
    sessions = relationship("UserSession", back_populates="user", cascade="all, delete-orphan")
    is_active = Column(Boolean, default=True, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)

    orders_rw_author = relationship("OrderRW", back_populates="author",
                                            foreign_keys='OrderRW.author_id')
    orders_rw_manager = relationship("OrderRW", back_populates="manager",
                                            foreign_keys='OrderRW.manager_id')


    @property
    def role_name(self):
        return self.role.name if self.role else None

    @property
    def formatted_created_at(self) -> str:
        return format_date(self.created_at)

    @property
    def formatted_updated_at(self) -> str:
        return format_date(self.updated_at)

    def __repr__(self):
        return f"<User(username={self.username}, email={self.email}, role_id={self.role_id})>"

class UserSession(Base):
    __tablename__ = "user_sessions"

    id = Column(Integer, primary_key=True, index=True)
    refresh_token = Column(String(255), nullable=False, unique=True)
    session_start = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    session_end = Column(DateTime(timezone=True), nullable=True)
    traffic = Column(Integer, default=0)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    user = relationship("User", back_populates="sessions")
    ip_address = Column(String(45), nullable=True)
    device_info = Column(String(255), nullable=True)

    @property
    def formatted_session_start(self) -> str:
        return format_date(self.session_start)

    @property
    def formatted_session_end(self) -> str:
        return format_date(self.session_end) if self.session_end else None

    def __repr__(self):
        return f"<UserSession(user_id={self.user_id}, refresh_token={self.refresh_token})>"

class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)
    description = Column(String(255), nullable=True)
    users = relationship("User", back_populates="role")

    def __repr__(self):
        return f"<Role(name={self.name})>"
