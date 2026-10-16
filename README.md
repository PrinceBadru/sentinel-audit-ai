# SentinelAudit-AI 🛡️

[![Live Interactive Demo](https://img.shields.io/badge/Live%20Demo-sentinel--audit--ai.vercel.app-10b981?style=for-the-badge&logo=vercel&logoColor=white)](https://sentinel-audit-ai.vercel.app)
[![GitHub Pages Demo](https://img.shields.io/badge/GitHub%20Pages-Live%20Simulation-0284c7?style=for-the-badge&logo=github&logoColor=white)](https://princebadru.github.io/sentinel-audit-ai/)

[![CI/CD Pipeline](https://github.com/PrinceBadru/sentinel-audit-ai/actions/workflows/ci.yml/badge.svg)](https://github.com/PrinceBadru/sentinel-audit-ai/actions)
[![Python 3.11](https://img.shields.io/badge/Python-3.11-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.92+-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Groq Llama 3.3](https://img.shields.io/badge/AI-Groq%20Llama%203.3%2070B-f55036)](https://groq.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> **Autonomous Enterprise Security & SOC2/OWASP Compliance Engine** built with Python 3.11, FastAPI, and Free-Tier LLM reasoning (Groq Llama 3.3 70B & Qwen 2.5 72B).

SentinelAudit-AI is an agentic platform designed to scan application source trees, detect high-risk vulnerabilities and compliance violations (OWASP Top 10, SOC2 Type II, HIPAA, PCI-DSS), compute weighted posture scores, and autonomously synthesize verified code remediation patches with zero cloud runtime costs.

---

## 🌐 Live Interactive Web App & Demo Walkthrough

Experience the full scanning and remediation engine live in your browser:
* **Production Deployment**: **[https://sentinel-audit-ai.vercel.app](https://sentinel-audit-ai.vercel.app)**
* **GitHub Pages Mirror**: **[https://princebadru.github.io/sentinel-audit-ai/](https://princebadru.github.io/sentinel-audit-ai/)**

### Interactive Capabilities in the Web App
1. **Pre-Loaded Vulnerability Scenarios**: Instantly test against real-world Fintech, E-Commerce, and Healthcare code snippets with exposed secrets, SQL injections, and wildcard CORS policies.
2. **Multi-Agent Pipeline Visualizer**: Watch real-time execution across the Scanner Agent (AST parsing), Triage Agent (CVSS posture scoring), and Remediation Agent (Groq AI diff generation).
3. **Side-by-Side Git Diff Viewer**: Compare original code with suggested fixes and click **"Apply Patch"** to update code in place and boost the compliance score to 100% (PASSED).
4. **Interactive Demo Tour**: Run an automated step-by-step video-style walkthrough demonstrating end-to-end vulnerability triage and remediation.
5. **Exportable Reports**: Generate and download formatted JSON or Markdown compliance audit summaries with one click.

---

## 🏛️ System Architecture

```mermaid
flowchart TD
    A[Client / CI Webhook / Web App] -->|POST /api/v1/audit| B[FastAPI Gateway]
    B --> C[Audit Orchestrator]
    
    subgraph Multi-Agent Core
        C --> D[Scanner Agent: AST & Regex Parser]
        D -->|Vulnerability Findings| E[Triage Agent: Risk & Posture Scoring]
        E -->|Prioritized Findings| F[Remediation Agent: Free Groq LLM Engine]
    end
    
    F -->|Patches & Diffs| G[Consolidated Audit Report]
    G --> B
    B -->|Structured JSON Response| A
```

---

## ✨ Key Capabilities

* **Multi-Framework Compliance**: Built-in rule sets spanning **OWASP Top 10** (SQLi, Wildcard CORS, Unsafe Deserialization), **SOC2 Type II** (Secret exposure, Hardcoded API keys), **HIPAA** (TLS verification), and **PCI-DSS** (Database credentials).
* **Autonomous Remediation**: Integrates with [Groq Cloud](https://console.groq.com) using free `llama-3.3-70b-versatile` to produce immediate git diff patches and mitigation guidance.
* **Zero-Cost Offline Fallback**: Deterministic AST remediation engine executes seamlessly in air-gapped CI/CD environments without external API keys or subscription fees.
* **Production Observability**: Built-in health checks (`/api/v1/health`), OpenAPI interactive documentation (`/docs`), and microsecond execution telemetry.

---

## 🚀 Quickstart

### 1. Local Setup
```bash
git clone https://github.com/PrinceBadru/sentinel-audit-ai.git
cd sentinel-audit-ai

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Configure Environment (Optional Free AI Key)
```bash
cp .env.example .env
# Add your free Groq API key from https://console.groq.com (optional; falls back seamlessly to deterministic engine)
export GROQ_API_KEY="gsk_..."
```

### 3. Run Development Server
```bash
uvicorn app.main:app --reload --port 8000
```
Interactive API documentation is live at `http://localhost:8000/docs`, and the interactive dashboard is served at `http://localhost:8000/`.

### 4. Run Test Suite
```bash
python -m unittest discover -s tests -p "test_*.py" -v
```

---

## 📡 API Usage Examples

### Quick Scan Snippet
```bash
curl -X POST "http://localhost:8000/api/v1/audit/quick" \
  -H "Content-Type: application/json" \
  -d '{
    "file_path": "auth.py",
    "code": "API_KEY = \"ghp_123456789012345678901234567890123456\"",
    "enable_ai_remediation": true
  }'
```

---

## 🐳 Docker Deployment

```bash
docker build -t sentinel-audit-ai:latest .
docker run -p 8000:8000 sentinel-audit-ai:latest
```

---

## 👨‍💻 Author
**Badru Ndawula**  
*Full-Stack Software Engineer & Cloud Systems Builder*  
* GitHub: [@PrinceBadru](https://github.com/PrinceBadru)  
* LinkedIn: [Badru Ndawula](https://www.linkedin.com/in/badru-ndawula-930b7b217)
* Live Application: [sentinel-audit-ai.vercel.app](https://sentinel-audit-ai.vercel.app)
