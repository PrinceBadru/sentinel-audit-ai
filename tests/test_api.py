import unittest
from starlette.testclient import TestClient
from app.main import app

class TestAPI(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_root_endpoint(self):
        res = self.client.get("/")
        self.assertEqual(res.status_code, 200)
        self.assertIn("version", res.json())

    def test_health_endpoint(self):
        res = self.client.get("/api/v1/health")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()["status"], "operational")

    def test_rules_endpoint(self):
        res = self.client.get("/api/v1/rules")
        self.assertEqual(res.status_code, 200)
        self.assertGreater(res.json()["count"], 0)

    def test_quick_scan_vulnerable_code(self):
        payload = {
            "file_path": "auth.py",
            "code": 'api_key = "sk-1234567890abcdef1234567890"',
            "enable_ai_remediation": True
        }
        res = self.client.post("/api/v1/audit/quick", json=payload)
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data["summary"]["critical_count"], 1)
        self.assertEqual(len(data["remediations"]), 1)
        self.assertIn("os.getenv", data["remediations"][0]["diff"])

if __name__ == "__main__":
    unittest.main()
