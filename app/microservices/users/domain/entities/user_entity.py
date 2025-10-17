from dataclasses import dataclass
import uuid

@dataclass
class UserEntity:
    id: uuid.UUID
    is_active: bool
    email: str
    password: str
    first_name: str
    last_name: str
