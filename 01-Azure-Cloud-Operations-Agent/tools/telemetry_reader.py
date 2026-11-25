import json
from pathlib import Path
from typing import Any


BASE_DIR = Path(__file__).resolve().parent.parent

DEFAULT_TELEMETRY_FILE = (
    BASE_DIR / "data" / "telemetry" / "sample_metrics.json"
)


class TelemetryReader:

    def __init__(self, file_path: Path = DEFAULT_TELEMETRY_FILE):
        self.file_path = Path(file_path)

    def read_metrics(self) -> dict[str, Any]:
        """
        Read Azure infrastructure telemetry from JSON.
        """

        if not self.file_path.exists():
            raise FileNotFoundError(
                f"Telemetry file not found: {self.file_path}"
            )

        try:
            with self.file_path.open("r", encoding="utf-8") as file:
                data = json.load(file)

        except json.JSONDecodeError as exc:
            raise ValueError(
                f"Invalid telemetry JSON: {exc}"
            ) from exc

        self._validate_metrics(data)

        return data

    @staticmethod
    def _validate_metrics(data: dict[str, Any]) -> None:
        """
        Validate required telemetry fields.
        """

        if not isinstance(data, dict):
            raise ValueError("Telemetry must be a JSON object")

        required_fields = [
            "resource",
            "resource_type",
            "environment",
            "location",
            "metrics",
            "status"
        ]

        for field in required_fields:
            if field not in data:
                raise ValueError(
                    f"Missing required field: {field}"
                )

        if not isinstance(data["metrics"], dict):
            raise ValueError("Metrics must be a JSON object")

        required_metrics = [
            "cpu_percent",
            "memory_percent",
            "disk_percent",
            "availability_percent",
            "http_5xx_count"
        ]

        for metric in required_metrics:
            if metric not in data["metrics"]:
                raise ValueError(
                    f"Missing required metric: {metric}"
                )

        metrics = data["metrics"]

        for metric in required_metrics:
            value = metrics[metric]

            if isinstance(value, bool) or not isinstance(value, (int, float)):
                raise ValueError(
                    f"Metric {metric} must be numeric"
                )

        for metric in [
            "cpu_percent",
            "memory_percent",
            "disk_percent",
            "availability_percent"
        ]:
            if not 0 <= metrics[metric] <= 100:
                raise ValueError(
                    f"Metric {metric} must be between 0 and 100"
                )

        if metrics["http_5xx_count"] < 0:
            raise ValueError(
                "http_5xx_count cannot be negative"
            )


if __name__ == "__main__":

    reader = TelemetryReader()

    try:
        telemetry = reader.read_metrics()

        print("\nAZURE TELEMETRY DATA")
        print("=" * 40)

        print(f"Resource: {telemetry['resource']}")
        print(f"Environment: {telemetry['environment']}")
        print(f"Location: {telemetry['location']}")

        print("\nMETRICS")
        print("=" * 40)

        for name, value in telemetry["metrics"].items():
            print(f"{name}: {value}")

        print(f"\nStatus: {telemetry['status']}")

    except (FileNotFoundError, ValueError) as error:
        print(f"ERROR: {error}")
        raise SystemExit(1)
