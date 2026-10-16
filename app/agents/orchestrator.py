import time
import uuid
from datetime import datetime, timezone
from typing import Dict, List
from app.models.schemas import AuditResponse
from app.core.scanner import CodeSecurityScanner
from app.agents.triage_agent import TriageAgent
from app.agents.remediation_agent import RemediationAgent

class AuditOrchestrator:
    """Multi-agent coordinator managing the end-to-end audit lifecycle."""

    def __init__(self):
        self.scanner = CodeSecurityScanner()
        self.triage_agent = TriageAgent()
        self.remediation_agent = RemediationAgent()

    async def execute_audit(self, target_name: str, files: Dict[str, str], enable_remediation: bool = True) -> AuditResponse:
        start_time = time.perf_counter()

        # Phase 1: Static Code Inspection
        findings = self.scanner.scan_repository(files)

        # Phase 2: Triage & Risk Scoring
        summary = self.triage_agent.evaluate(total_files=len(files), findings=findings)

        # Phase 3: AI-Driven Remediation Generation
        remediations = []
        if enable_remediation and findings:
            remediations = await self.remediation_agent.generate_patches(findings)

        elapsed_ms = round((time.perf_counter() - start_time) * 1000, 2)

        return AuditResponse(
            scan_id=f"SCAN-{uuid.uuid4().hex[:10].upper()}",
            target_name=target_name,
            timestamp=datetime.now(timezone.utc).isoformat(),
            summary=summary,
            findings=findings,
            remediations=remediations,
            execution_time_ms=elapsed_ms
        )
