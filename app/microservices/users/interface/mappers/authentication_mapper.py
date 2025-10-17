from app.microservices.users.domain.entities.user_entity import UserEntity
from app.microservices.users.infrastructure.models.user_model import User
from app.microservices.users.application.dtos.user_dto import UserDTO, UserPartialDTO
from app.microservices.users.interface.schemas.user_schema import UserRead, UserCreate, UserUpdate


class AuthenticationMapper:
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
    
    