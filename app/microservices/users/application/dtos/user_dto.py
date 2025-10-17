# app/schemas/user.py
from pydantic import BaseModel
from typing import Optional

class UserDTO(BaseModel):
    first_name: str
    last_name: str
    email: str 
    password: str


class UserPartialDTO(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]


class NotifyResetPasswordDTO(BaseModel):
    email: str
    reset_url: str