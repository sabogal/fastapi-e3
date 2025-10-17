# app/microservices/users/interface/controllers/auth_email_router.py
from fastapi import APIRouter, Depends
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from app.microservices.users.infrastructure.database.db_postgrest import get_async_session
from app.microservices.users.interface.schemas.user_schema import NotifyResetPassword 
from app.microservices.users.application.use_cases.reset_password_use_case import ResetPasswordUseCase
from app.microservices.users.infrastructure.repositories.user_repository import UserRepository
from app.microservices.users.infrastructure.services.email_notifier_service import EmailNotifierService
from app.microservices.users.infrastructure.repositories.password_reset_token_repository import PasswordResetTokenRepository
from app.microservices.users.interface.mappers.user_mapper import UserMapper


router = APIRouter()
DBSession = Annotated[AsyncSession, Depends(get_async_session)]

@router.post("/send_notify_reset_password", tags=["users"])
async def notify_reset_password(
    payload: NotifyResetPassword,
    db: DBSession,
):
    url_rediction = "http://example.com/reset_password?token={token}"
    use_case = ResetPasswordUseCase(
        UserRepository(db),
        PasswordResetTokenRepository(db),
        EmailNotifierService()
    )
    await use_case.notify(UserMapper.to_notify_reset_password_dto(payload.email, url_rediction))