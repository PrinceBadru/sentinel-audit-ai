import unittest
import asyncio
from app.agents.triage_agent import TriageAgent
from app.agents.remediation_agent import RemediationAgent
from app.models.schemas import VulnerabilityFinding, SeverityLevel, ComplianceFramework

class TestAgents(unittest.TestCase):
    def test_triage_score_calculation(self):
        triage = TriageAgent()
        finding = VulnerabilityFinding(
            id="VULN-001",
            rule_id="SEC-001",
            title="Hardcoded API Key",
            severity=SeverityLevel.CRITICAL,
            framework=ComplianceFramework.SOC2_TYPE_II,
            file_path="config.py",
            line_number=5,
            snippet='API_KEY = "ghp_123456789012345678901234567890123456"',
            description="Exposed secret"
        )
        summary = triage.evaluate(total_files=1, findings=[finding])
        self.assertEqual(summary.critical_count, 1)
        self.assertEqual(summary.compliance_score, 75.0)
        self.assertEqual(summary.status, "FAILED")

    def test_remediation_generation(self):
        async def run_async():
            remediation = RemediationAgent()
            finding = VulnerabilityFinding(
                id="VULN-002",
                rule_id="SEC-002",
                title="Permissive CORS",
                severity=SeverityLevel.HIGH,
                framework=ComplianceFramework.OWASP_TOP_10,
                file_path="main.py",
                line_number=10,
                snippet='allow_origins = ["*"]',
                description="Wildcard CORS"
            )
            patches = await remediation.generate_patches([finding])
            self.assertEqual(len(patches), 1)
            self.assertIn("allow_origins", patches[0].diff)
            self.assertGreater(patches[0].confidence_score, 0.9)
        asyncio.run(run_async())

if __name__ == "__main__":
    unittest.main()
