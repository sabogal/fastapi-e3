from app.microservices.users.domain.interfaces.repositories.i_user_repository import IUserRepository
from app.microservices.users.domain.interfaces.services.i_auth_service import IAuthService
from app.microservices.users.application.dtos.authentication_dtos import LoginDTO
from app.microservices.users.domain.exceptions.user_exception import CustomExcepcion



class AuthenticationUseCase:

    def __init__(self, user_repository: IUserRepository, authentication_service: IAuthService, password_helper):
        self.user_repository = user_repository
        self.authentication_service = authentication_service
        self.password_helper = password_helper

    async def authentication(self, dto: LoginDTO):
        user = await self.user_repository.get_by_email(dto.email)
        if not user:
            raise CustomExcepcion('No existe un usuario con ese email.')
        verified, _ = self.password_helper.verify_and_update(dto.password, user.password)
        if not verified:
            raise CustomExcepcion('Email o contraseña inválidos.')

        token = await self.authentication_service.login_with_email(dto.email, dto.password)
        return {"access_token": token, "token_type": "bearer"}