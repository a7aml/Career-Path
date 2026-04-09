from fastapi import APIRouter
from app.api.v1.endpoints import career, chat, users

api_router = APIRouter()

api_router.include_router(career.router, prefix="/career", tags=["Career"])
api_router.include_router(chat.router, prefix="/chat", tags=["Chat"])
api_router.include_router(users.router, prefix="/users", tags=["Users"])
