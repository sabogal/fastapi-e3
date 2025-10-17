from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, ForeignKey, DateTime, Boolean, Index
from app.microservices.users.infrastructure.models.user_model import User
from app.microservices.users.infrastructure.database.db_postgrest import Base
from sqlalchemy.dialects.postgresql import UUID
import uuid


class PasswordResetToken(Base):
    __tablename__ = "password_reset_tokens"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,              # genera UUID en la app
        # Si prefiere que lo genere la BD (requiere EXTENSION pgcrypto):
        # server_default=text("gen_random_uuid()"),
    )

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False)
    token: Mapped[str] = mapped_column(String(128), unique=True, index=True, nullable=False)
    used: Mapped[bool] = mapped_column(Boolean, default=False)
    used_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    user: Mapped["User"] = relationship("User")

Index("ix_password_reset_token_valid", PasswordResetToken.token, PasswordResetToken.used)

DEFAULT_EXP_MINUTES = 15

def generate_reset_token() -> str:
    return str(uuid.uuid4())

def token_expiry() -> datetime:
    return datetime.now(timezone.utc) + timedelta(minutes=DEFAULT_EXP_MINUTES)