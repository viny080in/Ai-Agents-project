from typing import Any


class IncidentClassifier:
    """
    Classify incidents into standardized severity levels.
    """

    SEVERITY_PRIORITY = {
        "CRITICAL": 1,
        "HIGH": 2,
        "MEDIUM": 3,
        "LOW": 4,
    }

    def classify(
        self,
        incidents: list[dict[str, Any]]
    ) -> list[dict[str, Any]]:

        classified = []

        for incident in incidents:

            item = incident.copy()

            incident_type = item.get("incident_type", "")
            observed = item.get("observed_value", 0)

            severity = item.get("severity", "LOW").upper()

            # Escalate severe infrastructure conditions
            if (
                incident_type == "High CPU Utilization"
                and observed >= 95
            ):
                severity = "CRITICAL"

            elif (
                incident_type == "High Memory Utilization"
                and observed >= 95
            ):
                severity = "CRITICAL"

            elif (
                incident_type == "High Disk Utilization"
                and observed >= 98
            ):
                severity = "CRITICAL"

            elif (
                incident_type == "Low Resource Availability"
                and observed < 95
            ):
                severity = "CRITICAL"

            elif (
                incident_type == "High HTTP 5xx Errors"
                and observed >= 100
            ):
                severity = "HIGH"

            item["severity"] = severity

            item["priority"] = (
                self.SEVERITY_PRIORITY.get(severity, 4)
            )

            item["status"] = "OPEN"

            item["assigned_team"] = "Azure Operations"

            classified.append(item)

        return sorted(
            classified,
            key=lambda x: x["priority"]
        )


if __name__ == "__main__":

    from telemetry_reader import TelemetryReader
    from incident_detector import IncidentDetector

    reader = TelemetryReader()
    telemetry = reader.read_metrics()

    detector = IncidentDetector()
    incidents = detector.detect_incidents(telemetry)

    classifier = IncidentClassifier()
    classified = classifier.classify(incidents)

    print("\nAZURE INCIDENT CLASSIFICATION REPORT")
    print("=" * 50)

    for index, incident in enumerate(classified, start=1):

        print(f"\nIncident #{index}")
        print(f"Type: {incident['incident_type']}")
        print(f"Severity: {incident['severity']}")
        print(f"Priority: P{incident['priority']}")
        print(f"Status: {incident['status']}")
        print(f"Assigned Team: {incident['assigned_team']}")

    print("\nTotal classified incidents:", len(classified))
