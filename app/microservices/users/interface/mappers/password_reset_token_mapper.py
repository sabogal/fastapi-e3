from app.microservices.users.domain.entities.password_reset_token_entity import PasswordResetTokenEntity
from app.microservices.users.infrastructure.models.reset_password_token_model import PasswordResetToken


class PasswordResetTokenMapper:
    @staticmethod
    def model_to_entity(token: PasswordResetToken):
        return PasswordResetTokenEntity(
            id=token.id,
            created_at=token.created_at,
            expires_at=token.expires_at,
            user_id=token.user_id,
            token=token.token,
            used=token.used,
            used_at=token.used_at
        )