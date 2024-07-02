from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from config.db import get_db
from api.dict.Operation.models import Operation
from api.dict.Operation.schemas import OperationInDBBase, OperationCreate, OperationUpdate, OperationRelate
from typing import List
from api.dict.Vat.schemas import VatInDBBase

router = APIRouter()


# Список
@router.get("/", response_model=List[OperationRelate])
async def read_operations(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(
            select(Operation)
            .options(selectinload(Operation.vat))
            .offset(skip).limit(limit)
        )
        operations = result.scalars().all()

        # Заполнение данных country_data для каждой организации
        for operation in operations:
            if operation.vat:
                operation.vat_data = VatInDBBase.from_orm(operation.vat)

        return operations

    except Exception as e:
        print(f"Ошибка чтения операции: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to read operations: {str(e)}")


@router.get("/{operation_id}", response_model=OperationRelate)
async def read_operation(operation_id: int, db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(
            select(Operation).options(selectinload(Operation.vat)).where(Operation.id == operation_id)
        )
        operation = result.scalars().one_or_none()
        if operation is None:
            raise HTTPException(status_code=404, detail="Operation not found")
        if operation.vat:
            operation.vat_data = VatInDBBase.from_orm(operation.vat)

        return OperationRelate.from_orm(operation)
    except Exception as e:
        print(f"Ошибка чтения операции: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to read operation: {str(e)}")


@router.post("/", response_model=OperationInDBBase)
async def create_or_update_operation(operation: OperationCreate, db: AsyncSession = Depends(get_db)):
    try:
        # Создаем новую запись
        new_operation = Operation(**operation.dict())
        db.add(new_operation)
        await db.commit()
        await db.refresh(new_operation)
        return OperationInDBBase.from_orm(new_operation)
    except Exception as e:
        print(f"Ошибка создания или обновления операции: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to create or update operation: {str(e)}")


@router.delete("/{operation_id}", response_model=OperationInDBBase)
async def delete_operation(operation_id: int, db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(
            select(Operation).where(Operation.id == operation_id)
        )
        operation = result.scalars().one_or_none()
        if operation is None:
            raise HTTPException(status_code=404, detail="Operation not found")

        await db.delete(operation)
        await db.commit()
        return OperationInDBBase.from_orm(operation)
    except Exception as e:
        print(f"Ошибка удаления операции: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to delete operation: {str(e)}")


@router.patch("/{operation_id}", response_model=OperationInDBBase)
async def update_operation(
        operation_id: int,
        operation_update: OperationUpdate,
        db: AsyncSession = Depends(get_db)
):
    try:
        result = await db.execute(
            select(Operation).where(Operation.id == operation_id)
        )
        existing_operation = result.scalars().one_or_none()

        if existing_operation is None:
            raise HTTPException(status_code=404, detail="Operation not found")

        for key, value in operation_update.dict(exclude_unset=True).items():
            setattr(existing_operation, key, value)

        await db.commit()
        await db.refresh(existing_operation)
        return OperationInDBBase.from_orm(existing_operation)
    except Exception as e:
        print(f"Ошибка частичного обновления операции: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to update operation: {str(e)}")
