from dataclasses import dataclass


@dataclass
class UserEntity:
    id: int
    is_active: bool
    email: str
    password: str
    first_name: str
    last_name: str
