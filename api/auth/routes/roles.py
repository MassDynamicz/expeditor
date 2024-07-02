# api/auth/routes/roles.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
<<<<<<< HEAD
from config.db import get_db
from api.auth import models, schemas
=======
from sqlalchemy.exc import IntegrityError
from config.db import get_db
from api.auth.models import Role
from api.auth.schemas import RoleCreate
>>>>>>> f474fef (Updated)
from typing import List

router = APIRouter()

<<<<<<< HEAD
@router.post("/", response_model=schemas.Role)
async def create_role(role: schemas.RoleCreate, db: AsyncSession = Depends(get_db)):
    try:
        print(f"Attempting to create role: {role.name}")
        result = await db.execute(select(models.Role).filter(models.Role.name == role.name))
        db_role = result.scalars().first()
        if db_role:
            raise HTTPException(status_code=400, detail="Role already exists")
        db_role = models.Role(**role.dict())
        db.add(db_role)
        await db.commit()
        await db.refresh(db_role)
        print(f"Role created with ID: {db_role.id}")
        return db_role
    except Exception as e:
        print(f"Error creating role: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.get("/", response_model=List[schemas.Role])
async def read_roles(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Role).offset(skip).limit(limit))
    roles = result.scalars().all()
    return roles

@router.get("/{role_id}", response_model=schemas.Role)
async def read_role(role_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Role).filter(models.Role.id == role_id))
    role = result.scalars().first()
    if role is None:
        raise HTTPException(status_code=404, detail="Role not found")
    return role

@router.put("/{role_id}", response_model=schemas.Role)
async def update_role(role_id: int, role: schemas.RoleCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Role).filter(models.Role.id == role_id))
    db_role = result.scalars().first()
    if db_role is None:
        raise HTTPException(status_code=404, detail="Role not found")
    db_role.name = role.name
    db_role.description = role.description
    await db.commit()
    await db.refresh(db_role)
    return db_role

@router.delete("/{role_id}", response_model=schemas.Role)
async def delete_role(role_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Role).filter(models.Role.id == role_id))
    db_role = result.scalars().first()
    if db_role is None:
        raise HTTPException(status_code=404, detail="Role not found")
    await db.delete(db_role)
    await db.commit()
    return db_role
=======
# Получаем роль
async def get_role(db: AsyncSession, role_name: str = "user") -> Role:
    result = await db.execute(select(Role).filter_by(name=role_name))
    role = result.scalars().first()

    # Если роли не определены, создаем "admin" при первой записи
    if not role:
        first_role = await db.execute(select(Role))
        if first_role.scalars().first() is None:
            role = Role(name="admin", description="Администратор")
        else:
            role = Role(name=role_name, description="Пользователи")
        db.add(role)
        await db.commit()
        await db.refresh(role)

    return role

@router.post("/", response_model=RoleCreate)
async def create_role(role: RoleCreate, db: AsyncSession = Depends(get_db)):
    existing_role = await db.execute(select(Role).filter_by(name=role.name))
    if existing_role.scalars().first():
        raise HTTPException(status_code=400, detail="Роль уже существует")
    
    new_role = Role(name=role.name, description=role.description)
    db.add(new_role)
    
    try:
        await db.commit()
        await db.refresh(new_role)
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Роль уже существует")
    
    return new_role

@router.get("/", response_model=List[RoleCreate])
async def read_roles(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Role).offset(skip).limit(limit))
    roles = result.scalars().all()
    return roles

@router.get("/{role_id}", response_model=RoleCreate)
async def read_role(role_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Role).filter_by(id=role_id))
    role = result.scalars().first()
    
    if not role:
        raise HTTPException(status_code=404, detail="Роль не найдена")
    
    return role
>>>>>>> f474fef (Updated)
