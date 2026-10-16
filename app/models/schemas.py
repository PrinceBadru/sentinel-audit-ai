from enum import Enum
from typing import List, Dict, Optional
from pydantic import BaseModel, Field

class SeverityLevel(str, Enum):
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"
    INFO = "INFO"

class ComplianceFramework(str, Enum):
    OWASP_TOP_10 = "OWASP_TOP_10"
    SOC2_TYPE_II = "SOC2_TYPE_II"
    HIPAA_SECURITY = "HIPAA_SECURITY"
    PCI_DSS = "PCI_DSS"

class VulnerabilityFinding(BaseModel):
    id: str
    rule_id: str
    title: str
    severity: SeverityLevel
    framework: ComplianceFramework
    file_path: str
    line_number: int
    snippet: str
    description: str
    cwe_id: Optional[str] = None

class RemediationPatch(BaseModel):
    finding_id: str
    rule_id: str
    file_path: str
    suggested_fix: str
    diff: str
    explanation: str
    confidence_score: float = Field(default=0.95, ge=0.0, le=1.0)

class AuditRequest(BaseModel):
    target_name: str = Field(..., example="Fintech Payments Core")
    files: Dict[str, str] = Field(..., description="Mapping of relative file path to file content")
    enable_ai_remediation: bool = Field(default=True, description="Whether to invoke LLM remediation generator")
    frameworks: List[ComplianceFramework] = Field(
        default=[ComplianceFramework.OWASP_TOP_10, ComplianceFramework.SOC2_TYPE_II]
    )

class QuickScanRequest(BaseModel):
    file_path: str = Field(default="snippet.py", example="auth.py")
    code: str = Field(..., example='password = "hardcoded_password_123"')
    enable_ai_remediation: bool = True

class AuditSummary(BaseModel):
    total_files_scanned: int
    total_findings: int
    critical_count: int
    high_count: int
    medium_count: int
    low_count: int
    info_count: int
    compliance_score: float = Field(..., description="Calculated 0-100 security compliance posture score")
    status: str = Field(..., example="PASSED or FAILED")

class AuditResponse(BaseModel):
    scan_id: str
    target_name: str
    timestamp: str
    summary: AuditSummary
    findings: List[VulnerabilityFinding]
    remediations: List[RemediationPatch]
    execution_time_ms: float

class HealthCheckResponse(BaseModel):
    status: str
    app_version: str
    groq_ai_connected: bool
    model: str
    timestamp: str
