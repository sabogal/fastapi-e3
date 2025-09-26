from ..entities.user_entity import UserEntity
from abc import ABC, abstractmethod


class IUserRepository(ABC):

    @abstractmethod
    def create(self, user: UserEntity) -> UserEntity: pass
        
    @abstractmethod
    def get_by_email(self, email: str) -> UserEntity: pass