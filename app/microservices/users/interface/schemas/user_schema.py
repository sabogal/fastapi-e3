# app/schemas/user.py
from pydantic import BaseModel
from typing import Optional


class UserCreateSchema(BaseModel):
    first_name: str
    last_name: str
    email: str 
    password: str


class UserUpdateSchema(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
