from app.microservices.users.domain.interfaces.repositories.i_password_reset_token_repository import IPasswordResetTokenRepository
from app.microservices.users.interface.mappers.password_reset_token_mapper import PasswordResetTokenMapper
from app.microservices.users.infrastructure.models.reset_password_token_model import PasswordResetToken, generate_reset_token, token_expiry
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timezone
from typing import Optional


class PasswordResetTokenRepository(IPasswordResetTokenRepository):

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, user_id: int) -> PasswordResetToken:
        row = PasswordResetToken(
            user_id=user_id,
            token=generate_reset_token(),
            expires_at=token_expiry(),
        )
        self.db.add(row)
        await self.db.flush()
        await self.db.commit()
        await self.db.refresh(row)
        return PasswordResetTokenMapper.model_to_entity(row)

    async def get_by_token_not_expired(self, token: str) -> Optional[PasswordResetToken]:
        now = datetime.now(timezone.utc)
        token = (
            await self.db.query(PasswordResetToken)
            .filter(
                PasswordResetToken.token == token,
                PasswordResetToken.expires_at > now,
            )
            .one_or_none()
        )
        return PasswordResetTokenMapper.model_to_entity(token) if token else None