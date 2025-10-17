# app/schemas/user.py
from pydantic import BaseModel
from typing import Optional


class LoginDTO(BaseModel):
    first_name: str
    last_name: str
    email: str 
    password: str
