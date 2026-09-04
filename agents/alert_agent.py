from datetime import datetime, timezone
from typing import Optional

from models.schemas import Alert, RiskAssessment


def build_alert(risk: RiskAssessment, previous_score: Optional[int] = None) -> Optional[Alert]:
    score_jump = previous_score is not None and risk.overall_score - previous_score >= 15
    if risk.overall_level in {"High", "Very High"} or score_jump:
        title = f"{risk.overall_level} environmental risk"
        message = risk.explanation
        return Alert(
            risk_level=risk.overall_level,
            title=title,
            message=message,
            timestamp=datetime.now(timezone.utc).isoformat(),
        )
    return None
