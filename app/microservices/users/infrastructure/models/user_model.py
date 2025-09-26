# app/infrastructure/database/models.py
from sqlalchemy import Column, Integer, String, Boolean
from app.microservices.users.infrastructure.database.db_postgrest import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    is_active = Column(Boolean, default=True)
    first_name = Column(String, index=True)
    last_name = Column(String)
    email = Column(String, unique=True, index=True)
    password = Column(String)

