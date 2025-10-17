from fastapi_users.password import PasswordHelper
from pwdlib import PasswordHash
from pwdlib.hashers.argon2 import Argon2Hasher
from app.microservices.users.domain.interfaces.services.i_password_service import IPasswordService


class PasswordService(IPasswordService):
    def __init__(self):
        self._password_hash = PasswordHash((Argon2Hasher(),))
        self._helper = PasswordHelper(self._password_hash)

    def hash(self, plain_password: str) -> str:
        if not plain_password:
            raise ValueError("La contraseña no puede estar vacía.")
        return self._helper.hash(plain_password)

    def verify(self, plain_password: str, hashed_password: str) -> bool:
        pass