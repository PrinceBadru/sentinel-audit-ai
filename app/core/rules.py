import re
from typing import Dict, Any, List
from app.models.schemas import SeverityLevel, ComplianceFramework

RULE_DEFINITIONS: List[Dict[str, Any]] = [
    {
        "id": "SEC-001",
        "title": "Hardcoded Cloud / API Secret Key",
        "severity": SeverityLevel.CRITICAL,
        "framework": ComplianceFramework.SOC2_TYPE_II,
        "cwe_id": "CWE-798",
        "description": "Hardcoded credential detected in source code. Secrets must be loaded via secure environment variables or a secrets vault.",
        "patterns": [
            r'(?i)(?:akia|asia)[0-9a-z]{16}',
            r'(?i)ghp_[a-zA-Z0-9]{36}',
            r'(?i)sk-[a-zA-Z0-9]{20,}',
            r'(?i)gsk_[a-zA-Z0-9]{20,}',
            r'(?i)(api[_-]?key|secret[_-]?key)\s*=\s*["\'][a-zA-Z0-9_-]{16,}["\']'
        ]
    },
    {
        "id": "SEC-002",
        "title": "Overly Permissive CORS Policy",
        "severity": SeverityLevel.HIGH,
        "framework": ComplianceFramework.OWASP_TOP_10,
        "cwe_id": "CWE-942",
        "description": "Access-Control-Allow-Origin is set to wildcard '*' with credentials or sensitive endpoints exposed, allowing unauthorized cross-origin data extraction.",
        "patterns": [
            r'allow_origins\s*=\s*\[\s*["\']\*["\']\s*\]',
            r'Access-Control-Allow-Origin["\']?\s*:\s*["\']\*["\']'
        ]
    },
    {
        "id": "SEC-003",
        "title": "SQL Injection via String Concatenation",
        "severity": SeverityLevel.CRITICAL,
        "framework": ComplianceFramework.OWASP_TOP_10,
        "cwe_id": "CWE-89",
        "description": "Unsanitized user inputs concatenated directly into dynamic SQL queries, bypassing ORM parameterized protections.",
        "patterns": [
            r'(?i)execute\(\s*f["\'].*SELECT.*FROM.*\{',
            r'(?i)cursor\.execute\(["\'].*WHERE.*\+\s*\w+',
            r'(?i)query\(\s*f["\'].*INSERT.*INTO'
        ]
    },
    {
        "id": "SEC-004",
        "title": "Insecure Deserialization via Unsafe Loader",
        "severity": SeverityLevel.HIGH,
        "framework": ComplianceFramework.OWASP_TOP_10,
        "cwe_id": "CWE-502",
        "description": "Untrusted deserialization can result in arbitrary remote code execution (RCE). Use yaml.safe_load() instead of pickle/unsafe yaml.",
        "patterns": [
            r'pickle\.loads\(',
            r'yaml\.load\([^,)]+\)'
        ]
    },
    {
        "id": "SEC-005",
        "title": "Disabled TLS/SSL Certificate Verification",
        "severity": SeverityLevel.HIGH,
        "framework": ComplianceFramework.HIPAA_SECURITY,
        "cwe_id": "CWE-295",
        "description": "Outbound HTTP requests disable certificate verification (verify=False), leaving network transit vulnerable to Man-In-The-Middle (MITM) attacks.",
        "patterns": [
            r'(?i)requests\.(get|post|put|delete)\(.*verify\s*=\s*False',
            r'(?i)httpx\.(get|post|put|delete|Client)\(.*verify\s*=\s*False'
        ]
    },
    {
        "id": "SEC-006",
        "title": "Hardcoded Password or Database Connection String",
        "severity": SeverityLevel.HIGH,
        "framework": ComplianceFramework.PCI_DSS,
        "cwe_id": "CWE-259",
        "description": "Database connection URI contains embedded plaintext user credentials.",
        "patterns": [
            r'(?i)postgres(?:ql)?:\/\/[a-z0-9_-]+:[a-z0-9_-]+@[a-z0-9_.-]+',
            r'(?i)mysql:\/\/[a-z0-9_-]+:[a-z0-9_-]+@[a-z0-9_.-]+',
            r'(?i)password\s*=\s*["\'][^"\']{6,}["\']'
        ]
    },
    {
        "id": "SEC-007",
        "title": "Exposed Debug Mode in Production Application",
        "severity": SeverityLevel.MEDIUM,
        "framework": ComplianceFramework.OWASP_TOP_10,
        "cwe_id": "CWE-489",
        "description": "Debug mode enabled exposes interactive stack traces, server environment, and internal memory schemas to attackers.",
        "patterns": [
            r'(?i)app\.run\(.*debug\s*=\s*True',
            r'(?i)DEBUG\s*=\s*True'
        ]
    }
]
