from dataclasses import dataclass
import uuid
from datetime import datetime
from typing import Optional
from app.microservices.users.domain.entities.user_entity import UserEntity


@dataclass
class PasswordResetTokenEntity:
    id: uuid.UUID
    created_at: datetime
    expires_at: datetime
    user_id: int
    token: str
    used: bool = False
    used_at: Optional[datetime] = None