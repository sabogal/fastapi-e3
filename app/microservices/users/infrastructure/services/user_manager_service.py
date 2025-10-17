# app/infrastructure/services/user_manager.py
import os, uuid
from typing import Optional
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi_users import BaseUserManager, UUIDIDMixin
from fastapi_users.exceptions import InvalidPasswordException
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase

from fastapi_users.password import PasswordHelper
from passlib.context import CryptContext

from app.microservices.users.infrastructure.database.db_postgrest import get_async_session
from app.microservices.users.infrastructure.models.user_model import User

SECRET = os.getenv("AUTH_SECRET", "CHANGE_ME_SUPER_SECRET")

# 1) Configurar Argon2 con Passlib
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")
argon2_helper = PasswordHelper(pwd_context)

class UserManager(UUIDIDMixin, BaseUserManager[User, uuid.UUID]):
    reset_password_token_secret = SECRET
    verification_token_secret = SECRET

    def __init__(self, user_db: SQLAlchemyUserDatabase):
        super().__init__(user_db)
        self.password_helper = argon2_helper

    async def validate_password(self, password: str, user: Optional[User] = None) -> None:
        if len(password) < 8:
            raise InvalidPasswordException("La contraseña debe tener al menos 8 caracteres")

async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)

async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)
