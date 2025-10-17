# app/interface/controllers/deps.py
import uuid
from fastapi_users import FastAPIUsers

from app.microservices.users.infrastructure.services.user_manager_service import get_user_manager, UserManager
from app.microservices.users.infrastructure.models.user_model import User
from app.microservices.users.infrastructure.services.authentication_service import auth_backend

fastapi_users = FastAPIUsers[User, uuid.UUID](
    get_user_manager,
    [auth_backend],
)

current_active_user = fastapi_users.current_user(active=True)
current_superuser = fastapi_users.current_user(active=True, superuser=True)


# app/api/deps/auth.py
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.microservices.users.infrastructure.services.authentication_service import get_jwt_strategy


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")  # ajusta si tu ruta de login es otra

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    user_manager: UserManager = Depends(get_user_manager),
):
    strategy = get_jwt_strategy()
    # Usa la MISMA estrategia que usas para emitir el token
    user = await strategy.read_token(token, user_manager)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o expirado",
        )
    # Si manejas estados (activo/bloqueado), valida aquí:
    # if not user.is_active:
    #     raise HTTPException(status_code=403, detail="Usuario inactivo")
    return user
