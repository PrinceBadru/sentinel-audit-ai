import unittest
from app.core.scanner import CodeSecurityScanner
from app.models.schemas import SeverityLevel

class TestScanner(unittest.TestCase):
    def setUp(self):
        self.scanner = CodeSecurityScanner()

    def test_detect_hardcoded_aws_key(self):
        vulnerable_code = 'AWS_SECRET = "AKIAIOSFODNN7EXAMPLE"'
        findings = self.scanner.scan_file("test_auth.py", vulnerable_code)
        self.assertEqual(len(findings), 1)
        self.assertEqual(findings[0].rule_id, "SEC-001")
        self.assertEqual(findings[0].severity, SeverityLevel.CRITICAL)

    def test_detect_sql_injection(self):
        vulnerable_code = 'cursor.execute(f"SELECT * FROM accounts WHERE id = {account_id}")'
        findings = self.scanner.scan_file("db.py", vulnerable_code)
        self.assertEqual(len(findings), 1)
        self.assertEqual(findings[0].rule_id, "SEC-003")

    def test_clean_file_produces_zero_findings(self):
        clean_code = '''
import os
api_key = os.getenv("API_KEY")
cursor.execute("SELECT * FROM accounts WHERE id = %s", (account_id,))
'''
        findings = self.scanner.scan_file("safe.py", clean_code)
        self.assertEqual(len(findings), 0)

if __name__ == "__main__":
    unittest.main()
