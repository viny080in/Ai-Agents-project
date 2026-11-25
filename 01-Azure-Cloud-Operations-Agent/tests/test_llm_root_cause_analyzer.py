from tools.llm_root_cause_analyzer import LLMRootCauseAnalyzer


def test_offline_analysis_generates_hypotheses():

    telemetry = {
        "resource": "azure-vm-web-01",
        "environment": "production",
        "metrics": {
            "cpu_percent": 92,
            "memory_percent": 88,
            "disk_percent": 76,
            "availability_percent": 99.2,
            "http_5xx_count": 45
        }
    }

    incidents = []

    analyzer = LLMRootCauseAnalyzer()

    report = analyzer.analyze(telemetry, incidents)

    assert report["analysis_status"] == "OFFLINE_SIMULATION"
    assert report["root_cause_confirmed"] is False
    assert len(report["root_cause_hypotheses"]) == 2

    for hypothesis in report["root_cause_hypotheses"]:
        assert hypothesis["cause"]
        assert hypothesis["evidence"]
        assert hypothesis["validation_steps"]
        assert hypothesis["remediation_actions"]


def test_offline_analysis_with_healthy_telemetry():

    telemetry = {
        "resource": "azure-vm-web-01",
        "environment": "production",
        "metrics": {
            "cpu_percent": 30,
            "memory_percent": 40,
            "disk_percent": 50,
            "availability_percent": 99.99,
            "http_5xx_count": 2
        }
    }

    analyzer = LLMRootCauseAnalyzer()

    report = analyzer.analyze(telemetry, [])

    assert report["analysis_status"] == "OFFLINE_SIMULATION"
    assert report["root_cause_confirmed"] is False
    assert report["root_cause_hypotheses"] == []
