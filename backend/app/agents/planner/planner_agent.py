class PlannerAgent:
    def decompose_task(self, prompt: str) -> dict:
        return {
            "prompt": prompt,
            "tasks": [
                "1. Analyze DataHub Metadata",
                "2. Perform Downstream Impact Analysis",
                "3. Generate FastAPI CRUD Router",
                "4. Generate SQLAlchemy Models & Alembic Migration",
                "5. Create Pytest cases"
            ]
        }
