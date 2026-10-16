from datetime import datetime, timezone
from fastapi import APIRouter, HTTPException
from app.models.schemas import (
    AuditRequest, QuickScanRequest, AuditResponse, HealthCheckResponse
)
from app.agents.orchestrator import AuditOrchestrator
from app.core.rules import RULE_DEFINITIONS
from app.core.groq_client import GroqLLMClient
from app.config import settings

router = APIRouter(prefix="/api/v1", tags=["Audit & Security"])
orchestrator = AuditOrchestrator()
groq_client = GroqLLMClient()

@router.get("/health", response_model=HealthCheckResponse)
async def health_check():
    ai_status = await groq_client.is_available()
    return HealthCheckResponse(
        status="operational",
        app_version=settings.APP_VERSION,
        groq_ai_connected=ai_status,
        model=settings.GROQ_MODEL,
        timestamp=datetime.now(timezone.utc).isoformat()
    )

@router.get("/rules")
async def list_rules():
    return {
        "count": len(RULE_DEFINITIONS),
        "rules": [
            {
                "id": r["id"],
                "title": r["title"],
                "severity": r["severity"],
                "framework": r["framework"],
                "description": r["description"],
                "cwe_id": r.get("cwe_id")
            }
            for r in RULE_DEFINITIONS
        ]
    }

@router.post("/audit", response_model=AuditResponse)
async def perform_audit(request: AuditRequest):
    if not request.files:
        raise HTTPException(status_code=400, detail="Audit request must contain at least one code file.")
    return await orchestrator.execute_audit(
        target_name=request.target_name,
        files=request.files,
        enable_remediation=request.enable_ai_remediation
    )

@router.post("/audit/quick", response_model=AuditResponse)
async def perform_quick_scan(request: QuickScanRequest):
    return await orchestrator.execute_audit(
        target_name=f"Quick Scan ({request.file_path})",
        files={request.file_path: request.code},
        enable_remediation=request.enable_ai_remediation
    )
