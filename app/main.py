from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.microservices.users.interface.controllers.deps import fastapi_users
from app.microservices.users.infrastructure.services.authentication_service import auth_backend

from app.microservices.users.interface.controllers.user_controller import router as users_router
from app.microservices.users.interface.controllers.authentication import router as auth_email_router
from app.microservices.users.interface.controllers.reset_password import router as reset_password_router

from app.microservices.users.infrastructure.database.db_postgrest import init_db, engine

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield
    await engine.dispose()

app = FastAPI(title="API", lifespan=lifespan)

# # --- Solo login (opcional, si quieres dejarlo activo) ---
# app.include_router(
#     fastapi_users.get_auth_router(auth_backend, requires_verification=False),
#     prefix="/auth/jwt",
#     tags=["auth"],
# )

app.include_router(
    auth_email_router, 
    prefix="/auth/jwt",
    tags=["auth"],
)

app.include_router(
    users_router,
    prefix="/api",
    tags=["users"],
)

app.include_router(
    reset_password_router,
    prefix="/api",
    tags=["users"],
)