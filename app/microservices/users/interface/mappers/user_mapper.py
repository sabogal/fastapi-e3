from app.microservices.users.domain.entities.user_entity import UserEntity
from app.microservices.users.infrastructure.models.user_model import User
from app.microservices.users.application.dtos.user_dto import UserDTO, UserPartialDTO
from app.microservices.users.interface.schemas.user_schema import UserCreateSchema


class UserMapper:
    @staticmethod
    def model_to_entity(user: User):
        return UserEntity(
            id=user.id,
            is_active=user.is_active,
            password=user.password,
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email
        )
    
    @classmethod
    def schema_to_dto(cls, user: UserCreateSchema, partial=False):
        if partial: 
            return cls.__partial_user_dto(user)
        return cls.__user_dto(user)
    
    def __user_dto(user: UserCreateSchema):
        return UserDTO(
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
            password=user.password
        )
    
    def __partial_user_dto(user: UserCreateSchema):
        return UserPartialDTO(
            first_name=user.first_name or None,
            last_name=user.last_name or None,
        )