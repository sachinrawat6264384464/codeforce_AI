class ContextAgent:
    def fetch_datahub_context(self, entity_name: str) -> dict:
        return {
            "entity": entity_name,
            "schema": ["id", "user_id", "status", "created_at"],
            "lineage": ["Upstream: PostgreSQL", "Downstream: Analytics Dashboard"],
            "ownership": "Core Engineering Team"
        }
