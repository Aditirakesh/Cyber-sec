import unittest
import sys
import os

# Ensure app is discoverable from tests directory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import app


class ReflectedXSSTests(unittest.TestCase):
    def setUp(self):
        app.config.update(
            TESTING=True,
            SECRET_KEY="test-secret"
        )
        self.client = app.test_client()

    def test_hub_page_loads(self):
        """Verify the hub page for Module 4 loads properly with READY status."""
        response = self.client.get("/xss_reflected/")
        self.assertEqual(response.status_code, 200)
        html = response.data.decode("utf-8")
        self.assertIn("Cross-Site Scripting (Reflected XSS)", html)
        self.assertIn("Vulnerable Search Portal", html)
        self.assertIn("Secure Search Portal", html)

    def test_normal_search_vuln(self):
        """Verify normal search returns matching resources on vulnerable endpoint."""
        response = self.client.get("/xss_reflected/vuln/?q=Python")
        self.assertEqual(response.status_code, 200)
        html = response.data.decode("utf-8")
        self.assertIn("Python Programming Master Notes", html)
        self.assertIn("CS-201", html)

    def test_normal_search_fixed(self):
        """Verify normal search returns matching resources on fixed endpoint."""
        response = self.client.get("/xss_reflected/fixed/?q=Python")
        self.assertEqual(response.status_code, 200)
        html = response.data.decode("utf-8")
        self.assertIn("Python Programming Master Notes", html)
        self.assertIn("CS-201", html)

    def test_vulnerable_endpoint_reflects_raw_script(self):
        """Verify vulnerable endpoint reflects unencoded script tag (XSS exploit)."""
        payload = "<script>alert('Reflected XSS')</script>"
        response = self.client.get(f"/xss_reflected/vuln/?q={payload}")
        self.assertEqual(response.status_code, 200)
        html = response.data.decode("utf-8")

        # The target span MUST contain the exact raw script tag
        self.assertIn(f'<span style="color:var(--danger);font-weight:700" id="reflectedTarget">{payload}</span>', html)

    def test_fixed_endpoint_escapes_script(self):
        """Verify fixed endpoint encodes HTML entities, preventing script execution."""
        payload = "<script>alert('Reflected XSS')</script>"
        response = self.client.get(f"/xss_reflected/fixed/?q={payload}")
        self.assertEqual(response.status_code, 200)
        html = response.data.decode("utf-8")

        # Must NOT contain raw script tag in reflectedTarget
        self.assertNotIn(f'<span style="color:var(--success);font-weight:700" id="reflectedTarget">{payload}</span>', html)
        # Must contain HTML escaped entities &lt;script&gt;
        self.assertIn("&lt;script&gt;alert(", html)


if __name__ == "__main__":
    unittest.main()

