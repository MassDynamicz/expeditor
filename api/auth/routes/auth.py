from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from config.db import get_db
from api.auth.models import User, UserSession
from config.utils import verify_password, create_access_token, SECRET_KEY, ALGORITHM
from datetime import timedelta, datetime
from jose import JWTError, jwt
from api.auth.schemas import User as UserSchema
from sqlalchemy.orm import selectinload

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
router = APIRouter()

# Обновляем сессию
async def update_user_session(token: str, db: AsyncSession, request: Request):
    result = await db.execute(select(UserSession).filter(UserSession.token == token))
    session = result.scalars().first()

    if session:
        # Update session end time and traffic
        session.session_end = datetime.utcnow()
        session.traffic += getattr(request.state, "request_size", 0) 
        await db.commit()
    else:
        raise HTTPException(status_code=401, detail="Session expired or not found")

    # Check if token is near expiration
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    exp = payload.get("exp")
    if exp and datetime.fromtimestamp(exp) < datetime.utcnow():
        raise HTTPException(status_code=401, detail="Token has expired")

# Авторизация
@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).filter(User.username == form_data.username))
    user = result.scalars().first()

    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неправильное имя пользователя или пароль",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Проверяем активную сессию
    result = await db.execute(
        select(UserSession).filter(UserSession.user_id == user.id, UserSession.session_end.is_(None))
    )
    active_session = result.scalars().first()

    if active_session:
        return {
            "access_token": active_session.token,
            "token_type": "bearer",
            "detail": "Уже авторизован"
        }

    # Создание токена и новой сессии
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user.username, "id": user.id, "email": user.email, "role": user.role_id},
        expires_delta=access_token_expires
    )

    user_session = UserSession(
        token=access_token,
        user_id=user.id,
    )
    db.add(user_session)
    await db.commit()

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "message": "Успешно авторизован"
    }

# Получение текущего пользователя
async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Не удалось проверить учетные данные",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        user_id: int = payload.get("id")
        email: str = payload.get("email")
        if username is None or user_id is None or email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    result = await db.execute(select(User).filter(User.id == user_id))
    user = result.scalars().first()
    if user is None:
        raise credentials_exception
    
    return user

# Получаем профиль пользователя
@router.get("/profile", response_model=UserSchema)
async def user_profile(request: Request,current_user: User = Depends(get_current_user),db: AsyncSession = Depends(get_db)):
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=400, detail="Authorization header missing or incorrect format")
    
    token = auth_header.split(" ")[1]
    await update_user_session(token, db, request)
    
    result = await db.execute(
        select(User)
        .options(selectinload(User.role), selectinload(User.sessions))
        .where(User.id == current_user.id)
    )
    user = result.scalars().first()
    
    if user is None:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    
    return UserSchema.from_orm(user)

# Выйти
@router.post("/logout")
async def logout(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):
    result = await db.execute(select(UserSession).filter(UserSession.token == token))
    session = result.scalars().first()

    if not session:
        raise HTTPException(status_code=404, detail="Сессия не найдена")

    session.session_end = datetime.utcnow()
    await db.commit()

    return {"detail": "Сессия завершена"}
