from typing import List
from app.models.schemas import VulnerabilityFinding, RemediationPatch
from app.core.groq_client import GroqLLMClient

class RemediationAgent:
    """Synthesizes contextual patches and explanations for detected findings."""

    def __init__(self, llm_client: GroqLLMClient = None):
        self.llm = llm_client or GroqLLMClient()

    async def generate_patches(self, findings: List[VulnerabilityFinding]) -> List[RemediationPatch]:
        patches: List[RemediationPatch] = []
        for finding in findings:
            res = await self.llm.generate_remediation(
                rule_id=finding.rule_id,
                title=finding.title,
                snippet=finding.snippet,
                file_path=finding.file_path
            )
            patch = RemediationPatch(
                finding_id=finding.id,
                rule_id=finding.rule_id,
                file_path=finding.file_path,
                suggested_fix=res["suggested_fix"],
                diff=res["diff"],
                explanation=res["explanation"],
                confidence_score=res.get("confidence_score", 0.95)
            )
            patches.append(patch)
        return patches
