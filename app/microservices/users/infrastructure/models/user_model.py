# app/infrastructure/database/models.py
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTableUUID
from app.microservices.users.infrastructure.database.db_postgrest import Base

class User(SQLAlchemyBaseUserTableUUID, Base):
    __tablename__ = "users"
    first_name: Mapped[str | None] = mapped_column(String(120))
    last_name:  Mapped[str | None] = mapped_column(String(120))
    # Hereda: id (UUID PK), email, hashed_password, is_active, is_superuser, is_verified
