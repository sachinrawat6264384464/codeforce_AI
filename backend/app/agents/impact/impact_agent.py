class ImpactAgent:
    def evaluate_impact(self, context: dict) -> dict:
        return {
            "risk_score": "MEDIUM",
            "affected_apis": 2,
            "affected_dashboards": 1,
            "breaking_change": False
        }
