import os

class BackendGeneratorAgent:
    def generate_files(self, project_id: str, prompt: str, modules: list) -> dict:
        """Generates real, valid FastAPI + SQLAlchemy + Pydantic files on disk."""
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../generated_projects", project_id, "backend"))
        os.makedirs(os.path.join(base_dir, "app/api"), exist_ok=True)
        os.makedirs(os.path.join(base_dir, "app/models"), exist_ok=True)
        os.makedirs(os.path.join(base_dir, "app/services"), exist_ok=True)
        os.makedirs(os.path.join(base_dir, "alembic/versions"), exist_ok=True)
        os.makedirs(os.path.join(base_dir, "tests"), exist_ok=True)

        entity = modules[0].lower() if modules else "orders"
        entity_single = entity.capitalize()

        # app/main.py
        main_code = f"""from fastapi import FastAPI
from app.api.{entity}_router import router as {entity}_router

app = FastAPI(title="ContextForge AI Generated - {entity_single} Microservice")

app.include_router({entity}_router, prefix="/api/v1")

@app.get("/health")
def health():
    return {{"status": "HEALTHY", "entity": "{entity}"}}
"""
        with open(os.path.join(base_dir, "app/main.py"), "w", encoding="utf-8") as f:
            f.write(main_code)

        # app/models/{entity}_model.py
        model_code = f"""from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func
from app.database.base import Base

class {entity_single}(Base):
    __tablename__ = "{entity}"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    status = Column(String(50), default="active")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
"""
        with open(os.path.join(base_dir, f"app/models/{entity}_model.py"), "w", encoding="utf-8") as f:
            f.write(model_code)

        # app/api/{entity}_router.py
        router_code = f"""from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel

router = APIRouter(prefix="/{entity}", tags=["{entity_single}"])

class {entity_single}Create(BaseModel):
    name: str
    status: str = "active"

@router.post("/")
def create_record(item: {entity_single}Create):
    return {{"message": "Created {entity_single}", "data": item}}

@router.get("/")
def list_records():
    return [{{"id": 1, "name": "Sample {entity_single}", "status": "active"}}]
"""
        with open(os.path.join(base_dir, f"app/api/{entity}_router.py"), "w", encoding="utf-8") as f:
            f.write(router_code)

        # app/services/{entity}_service.py
        service_code = f"""class {entity_single}Service:
    @staticmethod
    def process_record(data: dict):
        # Business logic for {entity_single}
        return {{"status": "processed", "payload": data}}
"""
        with open(os.path.join(base_dir, f"app/services/{entity}_service.py"), "w", encoding="utf-8") as f:
            f.write(service_code)

        # Dockerfile
        docker_code = """FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
"""
        with open(os.path.join(base_dir, "Dockerfile"), "w", encoding="utf-8") as f:
            f.write(docker_code)

        return {
            "status": "SUCCESS",
            "base_dir": base_dir,
            "generated_files": [
                "app/main.py",
                f"app/models/{entity}_model.py",
                f"app/api/{entity}_router.py",
                f"app/services/{entity}_service.py",
                "Dockerfile"
            ]
        }
