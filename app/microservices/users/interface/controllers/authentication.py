# app/microservices/users/interface/controllers/auth_email_router.py
from fastapi import APIRouter, Depends, HTTPException, status, Form
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from app.microservices.users.infrastructure.database.db_postgrest import get_async_session
from app.microservices.users.infrastructure.services.user_manager_service import get_user_manager, UserManager
from app.microservices.users.infrastructure.services.authentication_service import get_jwt_strategy
from app.microservices.users.infrastructure.services.authentication_service_2 import FastapiUsersAuthService
from app.microservices.users.application.use_cases.authentication_use_case import AuthenticationUseCase
from app.microservices.users.infrastructure.repositories.user_repository import UserRepository
from app.microservices.users.interface.schemas.user_schema import Login 


router = APIRouter()
DBSession = Annotated[AsyncSession, Depends(get_async_session)]

@router.post("/login", tags=["auth"])
async def login_with_email(
    payload: Login,
    db: DBSession,
    user_manager: UserManager = Depends(get_user_manager),
):
    use_case = AuthenticationUseCase(
        UserRepository(db),
        FastapiUsersAuthService(user_manager),
        user_manager.password_helper
    )
    use_case = await use_case.authentication(payload)
    return use_case