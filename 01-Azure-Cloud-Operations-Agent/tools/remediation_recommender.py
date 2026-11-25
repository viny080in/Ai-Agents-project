import json
from pathlib import Path
from typing import Any


class RemediationRecommender:

    def __init__(self, runbook_dir="data/runbooks"):
        self.runbook_dir = Path(runbook_dir)
        self.runbooks = {}

        self.load_runbooks()

    def load_runbooks(self):

        for file_path in self.runbook_dir.glob("*.json"):
            with open(file_path, "r", encoding="utf-8") as file:
                runbook = json.load(file)

            incident_type = runbook.get("incident_type")

            if incident_type:
                self.runbooks[incident_type] = runbook

    def recommend(
        self,
        incidents: list[dict[str, Any]]
    ) -> dict[str, Any]:

        recommendations = []

        for incident in incidents:

            incident_type = incident.get("incident_type")
            runbook = self.runbooks.get(incident_type)

            if not runbook:
                recommendations.append({
                    "incident_type": incident_type,
                    "status": "NO_RUNBOOK_FOUND",
                    "recommendations": []
                })
                continue

            recommendations.append({
                "incident_type": incident_type,
                "severity": incident.get("severity", "UNKNOWN"),
                "status": "RUNBOOK_MATCHED",
                "recommendations": runbook["recommendations"]
            })

        return {
            "recommendation_status": "SUCCESS",
            "total_incidents": len(incidents),
            "matched_runbooks": sum(
                1 for item in recommendations
                if item["status"] == "RUNBOOK_MATCHED"
            ),
            "recommendations": recommendations
        }
