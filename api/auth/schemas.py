from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

# Role Schemas
class RoleBase(BaseModel):
    id: int
    name: str
    description: Optional[str] = None

class RoleCreate(RoleBase):
    pass

class Role(RoleBase):
    id: int

    class Config:
        from_attributes = True

# UserSession Schemas
class UserSessionBase(BaseModel):
    refresh_token: str
    session_start: Optional[datetime] = None
    session_end: Optional[datetime] = None
    traffic: Optional[int] = 0
    ip_address: Optional[str] = None
    device_info: Optional[str] = None

class UserSessionCreate(UserSessionBase):
    user_id: int

class UserSession(UserSessionBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True

# User Schemas
class UserBase(BaseModel):
    username: str
    email: EmailStr
    is_active: Optional[bool] = None
    is_verified: Optional[bool] = None
    role_id: Optional[int] = None

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    company: Optional[str] = None
    is_active: Optional[bool] = None
    is_verified: Optional[bool] = None
    role_id: Optional[int] = None
    password: Optional[str] = None  # Добавлено поле для пароля
    old_password: Optional[str] = None  # Поле для старого пароля (для проверки)
    
class User(UserBase):
    id: int
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    company: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    is_active: bool
    is_verified: bool

    class Config:
        from_attributes = True

# Delete User
class UserDelete(BaseModel):
    detail: str
    user: User

    class Config:
        from_attributes = True

# Login Schema
class Login(BaseModel):
    username: str
    password: str

# Token Schema
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    user_id: Optional[str] = None
    username: Optional[str] = None
    role_id: int

class RefreshToken(BaseModel):
    token: str
    user_id: int
    expires_at: datetime
