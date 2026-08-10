from typing import Any, Dict
from fin_copilot.core.logging import logger


def validate_financial_output(raw_data: Dict[str, Any]) -> Dict[str, Any]:
    """Performs deterministic financial validation on query outputs."""
    anomalies = []

    if not raw_data:
        return {"is_valid": False, "anomalies": ["Empty dataset returned"], "confidence_score": 0.0}

    # Check for negative total amounts if present
    if "data" in raw_data and isinstance(raw_data["data"], list):
        for idx, row in enumerate(raw_data["data"]):
            for col, val in row.items():
                if "amount" in col.lower() or "revenue" in col.lower():
                    if isinstance(val, (int, float)) and val < 0:
                        anomalies.append(
                            f"Negative financial value in row {idx}, column '{col}': {val}"
                        )

    is_valid = len(anomalies) == 0
    logger.info(
        "Deterministic Financial Validation Completed",
        is_valid=is_valid,
        count_anomalies=len(anomalies),
    )

    return {"is_valid": is_valid, "anomalies": anomalies, "confidence_score": 1.0 if is_valid else 0.5}