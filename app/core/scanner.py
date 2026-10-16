import re
import uuid
from typing import List, Dict
from app.models.schemas import VulnerabilityFinding
from app.core.rules import RULE_DEFINITIONS

class CodeSecurityScanner:
    """High-performance multi-language static analysis engine."""

    def __init__(self, rules: List[Dict] = None):
        self.rules = rules or RULE_DEFINITIONS

    def scan_file(self, file_path: str, content: str) -> List[VulnerabilityFinding]:
        findings: List[VulnerabilityFinding] = []
        lines = content.splitlines()

        for rule in self.rules:
            matched_lines = set()
            for pattern_str in rule["patterns"]:
                pattern = re.compile(pattern_str)
                for line_idx, line in enumerate(lines, start=1):
                    if line_idx in matched_lines:
                        continue
                    if pattern.search(line):
                        matched_lines.add(line_idx)
                        finding = VulnerabilityFinding(
                            id=f"VULN-{uuid.uuid4().hex[:8].upper()}",
                            rule_id=rule["id"],
                            title=rule["title"],
                            severity=rule["severity"],
                            framework=rule["framework"],
                            file_path=file_path,
                            line_number=line_idx,
                            snippet=line.strip()[:140],
                            description=rule["description"],
                            cwe_id=rule.get("cwe_id")
                        )
                        findings.append(finding)

        return findings

    def scan_repository(self, files: Dict[str, str]) -> List[VulnerabilityFinding]:
        all_findings = []
        for file_path, content in files.items():
            all_findings.extend(self.scan_file(file_path, content))
        return all_findings
