# app/infrastructure/repositories/user_repository.py
from sqlalchemy.orm import Session
from contextlib import contextmanager
from app.microservices.users.domain.entities.user_entity import UserEntity
from app.microservices.users.domain.interfaces.i_user_repository import IUserRepository
from ..models.user_model import User
from app.microservices.users.interface.mappers.user_mapper import UserMapper
from app.microservices.users.application.dtos.user_dto import UserDTO, UserPartialDTO 




class UserRepository(IUserRepository):
    def __init__(self, db: Session):
        self.db = db

    def create(self, user: UserDTO) -> UserEntity:
        db_user = User(
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
            password=user.password
        )
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return UserMapper.model_to_entity(db_user)
    
    def get_all(self) -> list:
        instances = self.db.query(User).all()
        return [UserMapper.model_to_entity(instance) for instance in instances]
    
    def delete(self, pk: int) -> UserEntity:
        instance = self.db.query(User).filter(User.id == pk, User.is_active == True).first()
        if instance:
            instance.is_active = False
            self.db.add(instance)
            self.db.commit()
            self.db.refresh(instance)
            return UserMapper.model_to_entity(instance)
        return None

    def update(self, pk, user: UserPartialDTO):
        instance = self.db.query(User).filter(User.id == pk, User.is_active == True).first()
        data = user.model_dump(mode='json', exclude_none=True)
        if instance:
            for key, value in data.items():
                setattr(instance, key, value)
            self.db.commit()
            self.db.refresh(instance)
            return UserMapper.model_to_entity(instance)
        return None

    def get_by_email(self, email: str) -> UserEntity:
        instance = self.db.query(User).filter(User.email == email, User.is_active == True).first()
        if instance:
            return UserMapper.model_to_entity(instance)
        return None
    
    def get_by_id(self, pk: int) -> UserEntity:
        instance = self.db.query(User).filter(User.id == pk, User.is_active == True).first()
        if instance:
            return UserMapper.model_to_entity(instance)
        return None

