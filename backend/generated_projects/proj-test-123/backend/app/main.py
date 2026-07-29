from fastapi import FastAPI
from app.api.1. analyze datahub metadata_router import router as 1. analyze datahub metadata_router

app = FastAPI(title="ContextForge AI Generated - 1. analyze datahub metadata Microservice")

app.include_router(1. analyze datahub metadata_router, prefix="/api/v1")

@app.get("/health")
def health():
    return {"status": "HEALTHY", "entity": "1. analyze datahub metadata"}
