from ...entities.user_entity import UserEntity
from abc import ABC, abstractmethod


class IPasswordResetTokenRepository(ABC):

    @abstractmethod
    async def create(self, user_id: id) -> UserEntity: 
        raise NotImplementedError()
        
    @abstractmethod
    async def get_by_token_not_expired(self, token: str) -> UserEntity:
        raise NotImplementedError()

