from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from sqlalchemy.exc import IntegrityError
from sqlalchemy import delete, update
from config.db import get_db
from api.auth.models import Role, User, UserSession
from api.auth.routes.session import end_user_session
from api.auth.schemas import RoleCreate
from api.auth.routes.auth import role_required, user_status, get_current_user
from typing import List, Dict
from datetime import datetime

router = APIRouter()

# Получаем роль
async def get_role(db: AsyncSession, role_name: str = "user") -> Role:
    result = await db.execute(select(Role).filter_by(name=role_name))
    role = result.scalars().first()

    # Если роли не определены, создаем "admin", "user" и "guest" при первой записи
    if not role:
        first_role = await db.execute(select(Role))
        if first_role.scalars().first() is None:
            roles_to_create = [
                {"name": "admin", "description": "Администратор"},
                {"name": "user", "description": "Пользователь"},
                {"name": "guest", "description": "Гость"}
            ]
            for role_data in roles_to_create:
                new_role = Role(**role_data)
                db.add(new_role)
            await db.commit()
            # Возвращаем роль "admin" для первого пользователя
            role = await db.execute(select(Role).filter_by(name="admin"))
            role = role.scalars().first()
        else:
            role = Role(name=role_name, description="Пользователь")
            db.add(role)
            await db.commit()
            await db.refresh(role)

    return role

@router.post("/", response_model=RoleCreate)
async def create_role(role: RoleCreate, db: AsyncSession = Depends(get_db), current_user: User = role_required(["admin"])):
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
async def read_roles(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db), current_user: User = role_required(["admin"])):
    result = await db.execute(select(Role).offset(skip).limit(limit))
    roles = result.scalars().all()
    return roles

@router.get("/{role_id}", response_model=RoleCreate)
async def read_role(role_id: int, db: AsyncSession = Depends(get_db), current_user: User = role_required(["admin"])):
    result = await db.execute(select(Role).filter_by(id=role_id))
    role = result.scalars().first()
    
    if not role:
        raise HTTPException(status_code=404, detail="Роль не найдена")
    
    return role

@router.delete("/{role_id}", response_model=Dict[str, str])
async def delete_role(role_id: int, db: AsyncSession = Depends(get_db), current_user: User = role_required(["admin"])):
    try:
        # Предварительная загрузка данных
        role_result = await db.execute(
            select(Role).options(selectinload(Role.users)).filter_by(id=role_id)
        )
        role = role_result.scalars().first()

        if not role:
            raise HTTPException(status_code=404, detail="Роль не найдена")

        # Запрет на удаление ролей "администратор" и "пользователь"
        if role.name in ["admin", "user", "guest"]:
            raise HTTPException(status_code=403, detail=f"Роль '{role.description}' нельзя удалить")

        guest_role_result = await db.execute(
            select(Role).filter_by(name="guest")
        )
        guest_role = guest_role_result.scalars().first()

        if not guest_role:
            guest_role = Role(name="guest", description="Гость")
            db.add(guest_role)
            await db.commit()
            await db.refresh(guest_role)

        users = role.users

        async with db.begin():
            try:
                # Завершение сессий пользователей и обновление их роли до "гость"
                for user in users:
                    await end_user_session(user.id, db)
                    await db.execute(update(User).where(User.id == user.id).values(role_id=guest_role.id))

                await db.flush()

                # Удаление роли
                await db.execute(delete(Role).where(Role.id == role_id))

            except Exception as e:
                await db.rollback()
                raise HTTPException(status_code=500, detail=str(e))
            else:
                await db.commit()

        # Создание сообщения с информацией о перемещенных пользователях
        detail_message = (
            f"Роль с ID {role_id} успешно удалена. Пользователи перемещены в гостевую роль, сессии завершены"
        )

        return {"detail": detail_message}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))