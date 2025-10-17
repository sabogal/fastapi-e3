# app/infrastructure/repositories/user_repository.py
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.microservices.users.domain.entities.user_entity import UserEntity
from app.microservices.users.domain.interfaces.repositories.i_user_repository import IUserRepository
from ..models.user_model import User
from app.microservices.users.interface.mappers.user_mapper import UserMapper
from app.microservices.users.application.dtos.user_dto import UserDTO, UserPartialDTO


class UserRepository(IUserRepository):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, user: UserDTO) -> UserEntity:
        db_user = User(
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
            hashed_password=user.password,
        )
        self.db.add(db_user)
        await self.db.flush()
        await self.db.commit()
        await self.db.refresh(db_user)
        return UserMapper.model_to_entity(db_user)

    async def get_all(self) -> List[UserEntity]:
        stmt = select(User).where(User.is_active == True)
        result = await self.db.execute(stmt)
        instances = result.scalars().all()
        return [UserMapper.model_to_entity(instance) for instance in instances]

    async def delete(self, pk: int) -> Optional[UserEntity]:
        stmt = select(User).where(User.id == pk, User.is_active == True)
        result = await self.db.execute(stmt)
        instance = result.scalars().first()
        if not instance:
            return None

        instance.is_active = False
        await self.db.flush()
        await self.db.commit()
        await self.db.refresh(instance)
        return UserMapper.model_to_entity(instance)

    async def update(self, pk: int, user: UserPartialDTO) -> Optional[UserEntity]:
        stmt = select(User).where(User.id == pk, User.is_active == True)
        result = await self.db.execute(stmt)
        instance = result.scalars().first()
        if not instance:
            return None

        data = user.model_dump(mode="json", exclude_none=True)
        for key, value in data.items():
            if hasattr(instance, key):
                setattr(instance, key, value)

        await self.db.flush()
        await self.db.commit()
        await self.db.refresh(instance)
        return UserMapper.model_to_entity(instance)

    async def get_by_email(self, email: str) -> Optional[UserEntity]:
        stmt = select(User).where(User.email == email, User.is_active == True)
        result = await self.db.execute(stmt)
        instance = result.scalars().first()
        print("HOLA DESDE REPOSITORY")
        return UserMapper.model_to_entity(instance) if instance else None

    async def get_by_id(self, pk: int) -> Optional[UserEntity]:
        stmt = select(User).where(User.id == pk, User.is_active == True)
        result = await self.db.execute(stmt)
        instance = result.scalars().first()
        return UserMapper.model_to_entity(instance) if instance else None
