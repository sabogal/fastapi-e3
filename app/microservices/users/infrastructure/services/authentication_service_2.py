from fastapi import HTTPException, status
from app.microservices.users.domain.interfaces.services.i_auth_service import IAuthService
from app.microservices.users.infrastructure.services.user_manager_service import UserManager, get_user_manager
from app.microservices.users.infrastructure.services.authentication_service import get_jwt_strategy


class FastapiUsersAuthService(IAuthService):
    def __init__(self, user_manager: UserManager):
        self.user_manager = user_manager

    async def login_with_email(self, email: str, password: str) -> str:
        """
        Emite un JWT para el usuario dado.
        OJO: la verificación de contraseña ya se hizo en el use case.
        Aquí no se vuelve a verificar para evitar duplicidad.
        """
        user = await self.user_manager.get_by_email(email)
        if user is None:
            # Mantén tu excepción de dominio si prefieres
            raise ValueError("No existe un usuario con ese email.")

        strategy = get_jwt_strategy()
        token = await strategy.write_token(user)
        return token


# Factory de inyección (para Depends)
from fastapi import Depends
async def get_auth_service(user_manager: UserManager = Depends(get_user_manager)) -> IAuthService:
    return FastapiUsersAuthService(user_manager)