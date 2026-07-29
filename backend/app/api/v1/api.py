from fastapi import APIRouter
from app.api.v1 import auth_router, ws_router
from app.api.v1.projects import projects_router
from app.api.v1.generations import generations_router, chat_router
from app.api.v1.datahub import datahub_router
from app.api.v1.health import health_router
from app.api.v1 import database

api_router = APIRouter()
api_router.include_router(auth_router.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(projects_router.router, prefix="/projects", tags=["Projects"])
api_router.include_router(generations_router.router, prefix="/generations", tags=["AI Generations"])
api_router.include_router(chat_router.router, prefix="/generations", tags=["AI Copilot Chat"])
api_router.include_router(datahub_router.router, prefix="/datahub", tags=["DataHub Context"])
api_router.include_router(database.router, prefix="/database", tags=["Databases"])
api_router.include_router(health_router.router, prefix="/health", tags=["Health"])
api_router.include_router(ws_router.router, tags=["WebSocket Streaming"])
