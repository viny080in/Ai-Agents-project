import os
import json

from typing import Any
from openai import OpenAI
from dotenv import load_dotenv


load_dotenv(override=True)


class LLMRootCauseAnalyzer:

    def __init__(self):

        self.offline_mode = (
            os.getenv("LLM_OFFLINE_MODE", "false").lower() == "true"
        )

        self.client = None

        if not self.offline_mode:
            self.client = OpenAI(
                api_key=os.getenv("OPENAI_API_KEY")
            )

        self.model = os.getenv(
            "OPENAI_MODEL",
            "gpt-4.1-mini"
        )

    def analyze(
        self,
        telemetry: dict[str, Any],
        incidents: list[dict[str, Any]]
    ) -> dict[str, Any]:

        if self.offline_mode:

            metrics = telemetry["metrics"]

            hypotheses = []

            if metrics["cpu_percent"] > 85 or metrics["memory_percent"] > 85:
                hypotheses.append({
                    "cause": "Possible application resource exhaustion",
                    "description": "Elevated CPU or memory utilization indicates possible resource pressure.",
                    "evidence": [
                        f"CPU utilization: {metrics['cpu_percent']}%",
                        f"Memory utilization: {metrics['memory_percent']}%"
                    ],
                    "business_impact": "Potential application slowdown and degraded user experience.",
                    "confidence": "MEDIUM",
                    "validation_steps": [
                        "Inspect running processes.",
                        "Review application logs.",
                        "Check historical resource utilization."
                    ],
                    "remediation_actions": [
                        "Investigate resource-intensive processes.",
                        "Review application resource requirements."
                    ]
                })

            if metrics["http_5xx_count"] > 20:
                hypotheses.append({
                    "cause": "Possible application or dependency instability",
                    "description": "Elevated HTTP 5xx errors may indicate application or dependency failures.",
                    "evidence": [
                        f"HTTP 5xx errors: {metrics['http_5xx_count']}",
                        f"Availability: {metrics['availability_percent']}%"
                    ],
                    "business_impact": "Potential failed requests and reduced service reliability.",
                    "confidence": "MEDIUM",
                    "validation_steps": [
                        "Inspect application error logs.",
                        "Check dependency health.",
                        "Correlate errors with availability."
                    ],
                    "remediation_actions": [
                        "Investigate application exceptions.",
                        "Verify database and downstream service health."
                    ]
                })

            return {
                "analysis_status": "OFFLINE_SIMULATION",
                "root_cause_confirmed": False,
                "root_cause_hypotheses": hypotheses,
                "overall_impact": "Potential production service degradation.",
                "recommended_next_step": (
                    "Validate simulated hypotheses using application logs "
                    "and historical metrics."
                )
            }

        prompt = f"""
You are an Azure Cloud Operations and SRE expert.

Analyze this telemetry and classified incidents.

TELEMETRY:
{json.dumps(telemetry, indent=2)}

INCIDENTS:
{json.dumps(incidents, indent=2)}

Identify potential root causes, evidence, business impact,
confidence, validation steps and remediation actions.

Do not claim a root cause is confirmed without sufficient evidence.

Return valid JSON containing:
analysis_status,
root_cause_confirmed,
root_cause_hypotheses,
overall_impact,
recommended_next_step.
"""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert Azure SRE analyst. Return only valid JSON."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            response_format={"type": "json_object"},
            temperature=0.2
        )

        result = json.loads(
            response.choices[0].message.content
        )

        required_fields = [
            "analysis_status",
            "root_cause_confirmed",
            "root_cause_hypotheses",
            "overall_impact",
            "recommended_next_step"
        ]

        for field in required_fields:
            if field not in result:
                raise ValueError(f"Missing required field: {field}")

        return result
