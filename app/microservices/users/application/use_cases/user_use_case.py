from app.microservices.users.domain.entities.user_entity import UserEntity
from app.microservices.users.domain.interfaces.i_user_repository import IUserRepository
from app.microservices.users.application.dtos.user_dto import UserDTO
from app.microservices.users.domain.exceptions.user_exception import CustomExcepcion


class UserUseCase:

    def __init__(self, user_repository: IUserRepository):
        self.user_repository = user_repository

    def create(self, user: UserDTO) -> UserEntity:
        if self.user_repository.get_by_email(user.email):
            raise CustomExcepcion('El correo electrónico ya se encuentra registrado.', field='email')
        user_created = self.user_repository.create(user)
        if not user_created:
            raise CustomExcepcion('No se pudo crear el usuario.')
        return user_created
    
    def get_all(self):
        return self.user_repository.get_all()
    
    def update(self, pk: int, user: UserDTO) -> UserEntity:
        user = self.user_repository.update(pk, user)
        if not user:
            raise CustomExcepcion('No existe un usuario con ese ID.')
        return user
    
    def delete(self, pk: int) -> UserEntity:
        user = self.user_repository.delete(pk)
        if not user: 
            raise CustomExcepcion('No existe un usuario con ese ID.')
        return user
    
    def get_by_id(self, pk: int) -> UserEntity:
        user = self.user_repository.get_by_id(pk)
        if not user:
            raise CustomExcepcion('No existe un usuario con ese ID.')
        return user