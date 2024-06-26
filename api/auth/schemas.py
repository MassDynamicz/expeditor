# auth/schemas.py
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

# Permission Schemas
class PermissionBase(BaseModel):
    name: str
    description: Optional[str] = None

class PermissionCreate(PermissionBase):
    pass

class Permission(PermissionBase):
    id: int

    class Config:
        from_attributes = True

# Role Schemas
class RoleBase(BaseModel):
    name: str
    description: Optional[str] = None

class RoleCreate(RoleBase):
    pass

class Role(RoleBase):
    id: int
    permissions: List[Permission] = []

    class Config:
        from_attributes = True

# UserSession Schemas
class UserSessionBase(BaseModel):
    token: str
    session_start: Optional[datetime] = None
    session_end: Optional[datetime] = None
    traffic: Optional[int] = 0
    description: Optional[str] = None

class UserSessionCreate(UserSessionBase):
    pass

class UserSession(UserSessionBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True

# User Schemas
class UserBase(BaseModel):
    username: str
    email: str
    phone: Optional[str] = None
    role_id: Optional[int] = None


class UserCreate(UserBase):
    password: str

class UserUpdate(UserBase):
    username: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    email: Optional[str]
    phone: Optional[str]
    address: Optional[str]
    company: Optional[str]
    status: Optional[bool]
    password: Optional[str]

class User(UserBase):
    id: int
    role: Optional[Role] = None
    sessions: List[UserSession] = []

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
    user_id: int
    username: str
    role: Optional[str] = None

class TokenData(BaseModel):
    user_id: Optional[str] = None
    username: Optional[str] = None
    role: Optional[str] = None