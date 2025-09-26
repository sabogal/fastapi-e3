# main.py
from fastapi import FastAPI
from app.microservices.users.interface.controllers.user_controller import router as user_router

app = FastAPI()

app.include_router(user_router, prefix="/api", tags=["users"])