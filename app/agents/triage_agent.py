from typing import List
from app.models.schemas import VulnerabilityFinding, SeverityLevel, AuditSummary

class TriageAgent:
    """Calculates risk metrics, counts, and compliance posture scores."""

    SEVERITY_WEIGHTS = {
        SeverityLevel.CRITICAL: 25.0,
        SeverityLevel.HIGH: 10.0,
        SeverityLevel.MEDIUM: 4.0,
        SeverityLevel.LOW: 1.0,
        SeverityLevel.INFO: 0.0
    }

    def evaluate(self, total_files: int, findings: List[VulnerabilityFinding]) -> AuditSummary:
        crit = sum(1 for f in findings if f.severity == SeverityLevel.CRITICAL)
        high = sum(1 for f in findings if f.severity == SeverityLevel.HIGH)
        med = sum(1 for f in findings if f.severity == SeverityLevel.MEDIUM)
        low = sum(1 for f in findings if f.severity == SeverityLevel.LOW)
        info = sum(1 for f in findings if f.severity == SeverityLevel.INFO)

        # Baseline score 100 minus penalty weights
        penalty = (
            crit * self.SEVERITY_WEIGHTS[SeverityLevel.CRITICAL] +
            high * self.SEVERITY_WEIGHTS[SeverityLevel.HIGH] +
            med * self.SEVERITY_WEIGHTS[SeverityLevel.MEDIUM] +
            low * self.SEVERITY_WEIGHTS[SeverityLevel.LOW]
        )
        score = max(0.0, round(100.0 - penalty, 1))
        status = "FAILED" if crit > 0 or score < 70.0 else "PASSED"

        return AuditSummary(
            total_files_scanned=total_files,
            total_findings=len(findings),
            critical_count=crit,
            high_count=high,
            medium_count=med,
            low_count=low,
            info_count=info,
            compliance_score=score,
            status=status
        )
