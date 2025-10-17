# app/interfaces/api/user_api.py
import uuid
from fastapi import APIRouter, Depends, status, Path
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from app.microservices.users.application.use_cases.user_use_case import UserUseCase
from app.microservices.users.infrastructure.repositories.user_repository import UserRepository
from app.microservices.users.infrastructure.database.db_postgrest import get_async_session
from app.microservices.users.interface.mappers.user_mapper import UserMapper
from app.microservices.users.domain.exceptions.user_exception import CustomExcepcion
from app.microservices.users.interface.schemas.user_schema import UserRead, UserCreate, UserUpdate
from app.microservices.users.infrastructure.services.password_service import PasswordService
from app.microservices.users.interface.controllers.deps import get_current_user


router = APIRouter()
DBSession = Annotated[AsyncSession, Depends(get_async_session)]


@router.post("/users/")
async def create(user: UserCreate, db: DBSession):
    try:
        use_case = UserUseCase(UserRepository(db), PasswordService())
        new_user = await use_case.create(UserMapper.schema_to_dto(user))
        return new_user
    except CustomExcepcion as e: 
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=e.error
        )
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={'detail': str(e)}
        )
        
@router.patch("/users/{pk}")
async def update(
    user: UserUpdate,
    db: DBSession,
    pk: uuid.UUID = Path(..., description="ID del usuario"),
):
    try:
        use_case = UserUseCase(UserRepository(db))
        new_user = await use_case.update(pk, UserMapper.schema_to_dto(user, partial=True))
        return new_user
    except CustomExcepcion as e: 
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=e.error
        )
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={'detail': str(e)}
        )

@router.get("/users/")
async def get_all(
    db: DBSession,
    current_user = Depends(get_current_user),
):
    use_case = UserUseCase(UserRepository(db))
    users = await use_case.get_all()
    return users


@router.get("/users/{pk}")
async def get_by_id(db: DBSession, pk: uuid.UUID = Path(..., description="ID del usuario")):
    try:
        use_case = UserUseCase(UserRepository(db))
        user = await use_case.get_by_id(pk)
        return user
    except CustomExcepcion as e: 
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=e.error
        )
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={'detail': str(e)}
        )

@router.delete("/users/{pk}")
async def delete(db: DBSession, pk: uuid.UUID = Path(..., description="ID del usuario")):
    try:
        use_case = UserUseCase(UserRepository(db))
        await use_case.delete(pk)
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={'detail': 'Usuario eliminado con éxito.'}
        )
    except CustomExcepcion as e: 
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=e.error
        )
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={'detail': str(e)}
        )
