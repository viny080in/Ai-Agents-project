from tools.remediation_recommender import RemediationRecommender


def test_runbooks_load_successfully():
    recommender = RemediationRecommender()

    assert len(recommender.runbooks) == 5


def test_recommendations_match_incidents():
    recommender = RemediationRecommender()

    incidents = [
        {
            "incident_type": "High CPU Utilization",
            "severity": "HIGH"
        },
        {
            "incident_type": "High HTTP 5xx Errors",
            "severity": "HIGH"
        }
    ]

    report = recommender.recommend(incidents)

    assert report["recommendation_status"] == "SUCCESS"
    assert report["total_incidents"] == 2
    assert report["matched_runbooks"] == 2


def test_unknown_incident_has_no_runbook():
    recommender = RemediationRecommender()

    report = recommender.recommend([
        {"incident_type": "Unknown Incident"}
    ])

    assert report["matched_runbooks"] == 0
    assert report["recommendations"][0]["status"] == "NO_RUNBOOK_FOUND"
