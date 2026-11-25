from typing import Any


class RootCauseAnalyzer:
    """
    Analyze telemetry and incidents to generate
    evidence-based root cause hypotheses.
    """

    def analyze(
        self,
        telemetry: dict[str, Any],
        incidents: list[dict[str, Any]]
    ) -> dict[str, Any]:

        metrics = telemetry["metrics"]
        resource = telemetry["resource"]

        incident_types = {
            incident["incident_type"]
            for incident in incidents
        }

        hypotheses = []

        cpu = metrics["cpu_percent"]
        memory = metrics["memory_percent"]
        availability = metrics["availability_percent"]
        http_errors = metrics["http_5xx_count"]

        # Hypothesis 1: Application resource pressure
        if (
            "High CPU Utilization" in incident_types
            and "High Memory Utilization" in incident_types
        ):
            hypotheses.append({
                "cause": "Possible application resource exhaustion",
                "description": (
                    "High CPU and memory utilization may indicate "
                    "resource pressure on the virtual machine."
                ),
                "evidence": [
                    f"CPU utilization: {cpu}%",
                    f"Memory utilization: {memory}%"
                ],
                "validation_steps": [
                    "Inspect running processes and CPU consumption.",
                    "Review memory usage and application memory trends.",
                    "Check application logs for resource exhaustion."
                ]
            })

        # Hypothesis 2: Application or dependency instability
        if (
            http_errors > 20
            and availability < 99.9
        ):
            hypotheses.append({
                "cause": "Possible application or dependency instability",
                "description": (
                    "Elevated HTTP 5xx errors and reduced availability "
                    "may indicate application failures or unhealthy dependencies."
                ),
                "evidence": [
                    f"HTTP 5xx errors: {http_errors}",
                    f"Availability: {availability}%"
                ],
                "validation_steps": [
                    "Inspect application error logs.",
                    "Check application health endpoints.",
                    "Review database and downstream dependency health.",
                    "Correlate error timestamps with availability failures."
                ]
            })

        if not hypotheses:
            hypotheses.append({
                "cause": "Insufficient evidence to identify a likely cause",
                "description": (
                    "The available telemetry does not establish "
                    "a clear relationship between incidents."
                ),
                "evidence": [],
                "validation_steps": [
                    "Collect application logs.",
                    "Review historical performance metrics.",
                    "Inspect dependency and network health."
                ]
            })

        return {
            "resource": resource,
            "environment": telemetry["environment"],
            "incident_count": len(incidents),
            "analysis_status": "HYPOTHESES_GENERATED",
            "root_cause_confirmed": False,
            "hypotheses": hypotheses,
            "recommended_next_step": (
                "Validate the hypotheses using application logs, "
                "historical metrics and dependency health."
            )
        }


if __name__ == "__main__":

    from telemetry_reader import TelemetryReader
    from incident_detector import IncidentDetector
    from incident_classifier import IncidentClassifier

    reader = TelemetryReader()
    telemetry = reader.read_metrics()

    detector = IncidentDetector()
    incidents = detector.detect_incidents(telemetry)

    classifier = IncidentClassifier()
    classified_incidents = classifier.classify(incidents)

    analyzer = RootCauseAnalyzer()
    report = analyzer.analyze(
        telemetry,
        classified_incidents
    )

    print("\nAZURE ROOT CAUSE ANALYSIS REPORT")
    print("=" * 55)

    print(f"Resource: {report['resource']}")
    print(f"Environment: {report['environment']}")
    print(f"Incidents analyzed: {report['incident_count']}")
    print(f"Analysis status: {report['analysis_status']}")
    print(f"Root cause confirmed: {report['root_cause_confirmed']}")

    for index, hypothesis in enumerate(
        report["hypotheses"], start=1
    ):
        print(f"\nHypothesis #{index}")
        print(f"Possible cause: {hypothesis['cause']}")
        print(f"Description: {hypothesis['description']}")

        print("Evidence:")
        for evidence in hypothesis["evidence"]:
            print(f"  - {evidence}")

        print("Validation steps:")
        for step in hypothesis["validation_steps"]:
            print(f"  - {step}")

    print("\nRecommended next step:")
    print(report["recommended_next_step"])
