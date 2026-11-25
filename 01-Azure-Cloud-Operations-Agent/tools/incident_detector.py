from typing import Any


class IncidentDetector:
    """
    Detect infrastructure incidents using Azure telemetry.
    """

    DEFAULT_THRESHOLDS = {
        "cpu_percent": 85,
        "memory_percent": 85,
        "disk_percent": 90,
        "availability_percent": 99.9,
        "http_5xx_count": 20,
    }

    def __init__(self, thresholds: dict | None = None):
        self.thresholds = {
            **self.DEFAULT_THRESHOLDS,
            **(thresholds or {})
        }

    def detect_incidents(
        self,
        telemetry: dict[str, Any]
    ) -> list[dict[str, Any]]:

        metrics = telemetry.get("metrics", {})
        incidents = []

        resource = telemetry.get("resource", "unknown")

        # CPU detection
        cpu = metrics.get("cpu_percent")

        if cpu is not None and cpu > self.thresholds["cpu_percent"]:
            incidents.append({
                "incident_type": "High CPU Utilization",
                "severity": "HIGH",
                "resource": resource,
                "metric": "cpu_percent",
                "observed_value": cpu,
                "threshold": self.thresholds["cpu_percent"],
                "description": "CPU utilization exceeded the configured threshold."
            })

        # Memory detection
        memory = metrics.get("memory_percent")

        if memory is not None and memory > self.thresholds["memory_percent"]:
            incidents.append({
                "incident_type": "High Memory Utilization",
                "severity": "HIGH",
                "resource": resource,
                "metric": "memory_percent",
                "observed_value": memory,
                "threshold": self.thresholds["memory_percent"],
                "description": "Memory utilization exceeded the configured threshold."
            })

        # Disk detection
        disk = metrics.get("disk_percent")

        if disk is not None and disk > self.thresholds["disk_percent"]:
            incidents.append({
                "incident_type": "High Disk Utilization",
                "severity": "HIGH",
                "resource": resource,
                "metric": "disk_percent",
                "observed_value": disk,
                "threshold": self.thresholds["disk_percent"],
                "description": "Disk utilization exceeded the configured threshold."
            })

        # Availability detection
        availability = metrics.get("availability_percent")

        if (
            availability is not None
            and availability < self.thresholds["availability_percent"]
        ):
            incidents.append({
                "incident_type": "Low Resource Availability",
                "severity": "HIGH",
                "resource": resource,
                "metric": "availability_percent",
                "observed_value": availability,
                "threshold": self.thresholds["availability_percent"],
                "description": "Resource availability fell below the configured target."
            })

        # HTTP 5xx detection
        http_errors = metrics.get("http_5xx_count")

        if (
            http_errors is not None
            and http_errors > self.thresholds["http_5xx_count"]
        ):
            incidents.append({
                "incident_type": "High HTTP 5xx Errors",
                "severity": "MEDIUM",
                "resource": resource,
                "metric": "http_5xx_count",
                "observed_value": http_errors,
                "threshold": self.thresholds["http_5xx_count"],
                "description": "HTTP server errors exceeded the configured threshold."
            })

        return incidents


if __name__ == "__main__":

    from telemetry_reader import TelemetryReader

    reader = TelemetryReader()
    telemetry = reader.read_metrics()

    detector = IncidentDetector()
    incidents = detector.detect_incidents(telemetry)

    print("\nAZURE INCIDENT DETECTION REPORT")
    print("=" * 45)

    print(f"Resource: {telemetry['resource']}")
    print(f"Total incidents detected: {len(incidents)}")

    for index, incident in enumerate(incidents, start=1):
        print(f"\nIncident #{index}")
        print(f"Type: {incident['incident_type']}")
        print(f"Severity: {incident['severity']}")
        print(f"Metric: {incident['metric']}")
        print(f"Observed: {incident['observed_value']}")
        print(f"Threshold: {incident['threshold']}")
        print(f"Description: {incident['description']}")
