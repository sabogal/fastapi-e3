import uuid
from pydantic import BaseModel, EmailStr, Field
from pydantic import ConfigDict


class UserRead(BaseModel):
    id: uuid.UUID
    email: EmailStr
    is_active: bool
    is_superuser: bool
    is_verified: bool
    first_name: str | None = None
    last_name: str | None = None

    # Permite crear este modelo a partir de objetos ORM (SQLAlchemy)
    model_config = ConfigDict(from_attributes=True)


class UserCreate(BaseModel):
    email: EmailStr = Field(..., description="Correo del usuario")
    password: str = Field(..., min_length=8, description="Contraseña en texto plano; se hashea en el backend")
    first_name: str | None = Field(None, max_length=120)
    last_name: str | None = Field(None, max_length=120)


class UserUpdate(BaseModel):
    first_name: str | None = Field(None, max_length=120)
    last_name: str | None = Field(None, max_length=120)


class NotifyResetPassword(BaseModel):
    email: EmailStr

class Login(BaseModel):
    email: str 
    password: str