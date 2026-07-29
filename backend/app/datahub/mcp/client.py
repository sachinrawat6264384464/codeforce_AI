class DataHubMCPClient:
    def __init__(self, gms_url: str = "http://localhost:8080"):
        self.gms_url = gms_url

    def get_entity_metadata(self, entity_urn: str) -> dict:
        return {
            "urn": entity_urn,
            "type": "dataset",
            "platform": "postgres",
            "status": "connected"
        }
