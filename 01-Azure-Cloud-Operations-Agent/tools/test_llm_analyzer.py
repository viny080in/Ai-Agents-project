import json

from unittest.mock import patch, MagicMock

from telemetry_reader import TelemetryReader
from incident_detector import IncidentDetector
from incident_classifier import IncidentClassifier
from llm_root_cause_analyzer import LLMRootCauseAnalyzer


def main():

    reader = TelemetryReader()
    telemetry = reader.read_metrics()

    detector = IncidentDetector()
    incidents = detector.detect_incidents(telemetry)

    classifier = IncidentClassifier()
    classified_incidents = classifier.classify(incidents)

    mock_report = {
        "analysis_status": "AI_ANALYSIS_COMPLETED",
        "root_cause_confirmed": False,
        "root_cause_hypotheses": [
            {
                "cause": "Possible application resource exhaustion",
                "description": "High CPU and memory utilization.",
                "evidence": [
                    "CPU utilization: 92%",
                    "Memory utilization: 88%"
                ],
                "business_impact": "Potential application slowdown.",
                "confidence": "MEDIUM",
                "validation_steps": [
                    "Inspect application logs."
                ],
                "remediation_actions": [
                    "Investigate resource-intensive processes."
                ]
            }
        ],
        "overall_impact": "Production application performance degradation.",
        "recommended_next_step": "Validate hypotheses using application logs."
    }

    mock_response = MagicMock()
    mock_response.choices[0].message.content = json.dumps(mock_report)

    analyzer = LLMRootCauseAnalyzer()

    with patch.object(
        analyzer.client.chat.completions,
        "create",
        return_value=mock_response
    ):

        report = analyzer.analyze(
            telemetry,
            classified_incidents
        )

    print("\nOFFLINE AI ROOT CAUSE ANALYSIS")
    print("=" * 50)

    print(json.dumps(report, indent=2))

    assert report["analysis_status"] == "AI_ANALYSIS_COMPLETED"
    assert report["root_cause_confirmed"] is False
    assert len(report["root_cause_hypotheses"]) > 0

    print("\nTEST PASSED")


if __name__ == "__main__":
    main()
