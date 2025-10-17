from app.microservices.users.domain.entities.user_entity import UserEntity
from app.microservices.users.domain.interfaces.repositories.i_user_repository import IUserRepository
from app.microservices.users.application.dtos.user_dto import UserDTO
from app.microservices.users.domain.exceptions.user_exception import CustomExcepcion
from app.microservices.users.infrastructure.services.password_service import PasswordService

class UserUseCase:

    def __init__(self, user_repository: IUserRepository, password_service: PasswordService = None):
        self.user_repository = user_repository
        self.password_service = password_service

    async def create(self, user: UserDTO) -> UserEntity:
        if await self.user_repository.get_by_email(user.email):
            raise CustomExcepcion('El correo electrónico ya se encuentra registrado.', field='email')

        user.password = self.password_service.hash(user.password)
        user_created = await self.user_repository.create(user)
        if not user_created:
            raise CustomExcepcion('No se pudo crear el usuario.')
        return user_created

    async def get_all(self):
        return await self.user_repository.get_all()

    async def update(self, pk: int, user: UserDTO) -> UserEntity:
        user = await self.user_repository.update(pk, user)
        if not user:
            raise CustomExcepcion('No existe un usuario con ese ID.')
        return user

    async def delete(self, pk: int) -> UserEntity:
        user = await self.user_repository.delete(pk)
        if not user:
            raise CustomExcepcion('No existe un usuario con ese ID.')
        return user

    async def get_by_id(self, pk: int) -> UserEntity:
        user = await self.user_repository.get_by_id(pk)
        if not user:
            raise CustomExcepcion('No existe un usuario con ese ID.')
        return user