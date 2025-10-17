from app.microservices.users.domain.entities.user_entity import UserEntity
from app.microservices.users.infrastructure.models.user_model import User
from app.microservices.users.application.dtos.user_dto import UserDTO, UserPartialDTO
from app.microservices.users.interface.schemas.user_schema import UserRead, UserCreate, UserUpdate


class UserMapper:
    @staticmethod
    def model_to_entity(user: User):
        return UserEntity(
            id=user.id,
            is_active=user.is_active,
            password=user.hashed_password,
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email
        )
    
    @classmethod
    def schema_to_dto(cls, user: UserCreate, partial=False):
        if partial: 
            return cls.__partial_user_dto(user)
        return cls.__user_dto(user)
    
    def __user_dto(user: UserCreate):
        return UserDTO(
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
            password=user.password
        )
    
    def __partial_user_dto(user: UserCreate):
        return UserPartialDTO(
            first_name=user.first_name or None,
            last_name=user.last_name or None,
        )
    
    def to_notify_reset_password_dto(email: str, reset_url: str):
        from app.microservices.users.application.dtos.user_dto import NotifyResetPasswordDTO
        return NotifyResetPasswordDTO(
            email=email,
            reset_url=reset_url
        )
    