import re

from models.schemas import Advisory, RiskAssessment

BLOCKED_PATTERNS = [
    r"\byou have\b",
    r"\bdiagnos",
    r"\btake\s+\w+\s+(tablet|pill|medicine)\b",
    r"\bstop\s+(your|the)\s+medication\b",
]


def validate_advisory_safety(advisory: Advisory, risk: RiskAssessment) -> bool:
    text = " ".join(
        [
            advisory.summary,
            " ".join(advisory.actions),
            advisory.outdoor_guidance,
            advisory.personalization_reason,
        ]
    ).lower()
    if any(re.search(pattern, text) for pattern in BLOCKED_PATTERNS):
        return False

    if risk.overall_level in {"High", "Very High"} and len(advisory.actions) < 2:
        return False

    return True
