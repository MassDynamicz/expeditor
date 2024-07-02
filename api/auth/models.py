<<<<<<< HEAD
# auth/models.py
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from config.db import Base

role_permissions = Table(
    'role_permissions', Base.metadata,
    Column('role_id', Integer, ForeignKey('roles.id'), primary_key=True),
    Column('permission_id', Integer, ForeignKey('permissions.id'), primary_key=True)
)

=======
from sqlalchemy import (
    Column, Integer, String, Boolean, DateTime, ForeignKey, BigInteger
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from enum import Enum
from config.db import Base

class UserStatus(Enum):
    ACTIVE = "Активен"
    INACTIVE = "Отключен"
>>>>>>> f474fef (Updated)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
<<<<<<< HEAD
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, unique=True, index=True, nullable=False)
    phone = Column(String)
    address = Column(String)
    company = Column(String)
    status = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), nullable=True)
    role_id = Column(Integer, ForeignKey('roles.id'))
    role = relationship("Role", back_populates="users")
    sessions = relationship("UserSession", back_populates="user", cascade="all, delete-orphan")

=======
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    email = Column(String, unique=True, nullable=False)
    phone = Column(String, nullable=True)
    address = Column(String, nullable=True)
    company = Column(String, nullable=True)
    status = Column(String, default=UserStatus.INACTIVE.value, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    role_id = Column(Integer, ForeignKey('roles.id'), nullable=True)
    role = relationship("Role", back_populates="users")
    sessions = relationship("UserSession", back_populates="user", cascade="all, delete-orphan")

    @property
    def role_name(self):
        # Ensure this property does not perform synchronous database access
        return self.role.name if self.role else None

    def __repr__(self):
        return f"<User(username={self.username}, email={self.email}, role_id={self.role_id})>"
>>>>>>> f474fef (Updated)

class UserSession(Base):
    __tablename__ = "user_sessions"

    id = Column(Integer, primary_key=True, index=True)
<<<<<<< HEAD
    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    token = Column(String, nullable=False)
    session_start = Column(DateTime(timezone=True), server_default=func.now())
    session_end = Column(DateTime(timezone=True), nullable=True)
    traffic = Column(Integer, default=0)
    user = relationship("User", back_populates="sessions")

=======
    token = Column(String(255), nullable=False, unique=True)
    session_start = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    session_end = Column(DateTime(timezone=True), nullable=True)
    traffic = Column(BigInteger, default=0)
    user = relationship("User", back_populates="sessions")
    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    
    def __repr__(self):
        return f"<UserSession(user_id={self.user_id}, token={self.token})>"
>>>>>>> f474fef (Updated)

class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
<<<<<<< HEAD
    name = Column(String, unique=True, nullable=False)
    description = Column(String)
    users = relationship("User", back_populates="role")
    permissions = relationship("Permission", secondary=role_permissions, back_populates="roles")


class Permission(Base):
    __tablename__ = "permissions"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(String)
    roles = relationship("Role", secondary=role_permissions, back_populates="permissions")
=======
    name = Column(String(50), unique=True, nullable=False)
    description = Column(String(255), nullable=True)
    
    users = relationship("User", back_populates="role")

    def __repr__(self):
        return f"<Role(name={self.name})>"
>>>>>>> f474fef (Updated)
