# app/infrastructure/services/auth.py
from fastapi_users.authentication import AuthenticationBackend, BearerTransport, JWTStrategy
from app.microservices.users.infrastructure.services.user_manager_service import SECRET

bearer_transport = BearerTransport(tokenUrl="/auth/jwt/login")

def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET, lifetime_seconds=60 * 60)  # 1 hora

auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)
