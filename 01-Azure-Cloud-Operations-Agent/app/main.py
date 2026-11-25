from fastapi import FastAPI, HTTPException

from tools.telemetry_reader import TelemetryReader
from tools.incident_detector import IncidentDetector
from tools.incident_classifier import IncidentClassifier
from tools.llm_root_cause_analyzer import LLMRootCauseAnalyzer
from tools.remediation_recommender import RemediationRecommender


app = FastAPI(
    title="Azure Cloud Operations Agent",
    description="AI-powered Azure infrastructure monitoring and root cause analysis",
    version="2.0.0",
)


@app.get("/")
async def root():
    return {
        "project": "Azure Cloud Operations Agent",
        "status": "running",
        "environment": "local-simulation",
    }


@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "azure_connection": "not_configured",
        "mode": "simulation",
    }


@app.get("/analyze")
async def analyze_incidents():

    try:
        reader = TelemetryReader()
        telemetry = reader.read_metrics()

        detector = IncidentDetector()
        incidents = detector.detect_incidents(telemetry)

        classifier = IncidentClassifier()
        classified_incidents = classifier.classify(incidents)

        analyzer = LLMRootCauseAnalyzer()

        recommender = RemediationRecommender()
        remediation = recommender.recommend(classified_incidents)

        report = analyzer.analyze(
            telemetry,
            classified_incidents
        )

        return {
            "resource": telemetry["resource"],
            "incident_count": len(classified_incidents),
            "incidents": classified_incidents,
            "ai_analysis": report,
            "remediation": remediation,
        }

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=str(error)
        )
