import os
from app.microservices.users.domain.interfaces.repositories.i_user_repository import IUserRepository
from app.microservices.users.domain.interfaces.repositories.i_password_reset_token_repository import IPasswordResetTokenRepository
from app.microservices.users.domain.interfaces.services.i_email_notifier_service import IEmailNotifierService
from app.microservices.users.application.dtos.user_dto import NotifyResetPasswordDTO
from app.microservices.users.domain.exceptions.user_exception import CustomExcepcion



class ResetPasswordUseCase:

    def __init__(self, user_repository: IUserRepository, password_reset_token_repository: IPasswordResetTokenRepository, notification_service: IEmailNotifierService):
        self.user_repository = user_repository
        self.password_reset_token_repository = password_reset_token_repository
        self.notification_service = notification_service

    async def notify(self, dto: NotifyResetPasswordDTO):
        user = await self.user_repository.get_by_email(dto.email)
        if not user:
            raise CustomExcepcion('No existe un usuario con ese email.')
        token = await self.password_reset_token_repository.create(user.id)
        await self.notification_service.send_email(
            template="reset_password.html",
            title="Restablecer contraseña",
            to=[dto.email],
            content={
                "name": "prueba",
                "reset_url": dto.reset_url.format(token=token.token),
            }
        )