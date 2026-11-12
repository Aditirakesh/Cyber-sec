import unittest

from app import app


class CSRFModuleTests(unittest.TestCase):
    def setUp(self):
        app.config.update(
            TESTING=True,
            SECRET_KEY="test-secret",
            SESSION_COOKIE_SECURE=False,
            SESSION_COOKIE_SAMESITE="Lax",
        )
        self.client = app.test_client()
        self.client.get("/csrf/")

    def _state(self):
        with self.client.session_transaction() as sess:
            return sess["csrf_balance"], sess["csrf_token"]

    def test_vulnerable_post_without_token_succeeds(self):
        before, _ = self._state()
        response = self.client.post(
            "/csrf/vuln/transfer",
            data={"recipient": "Attacker demo account", "amount": "500"},
        )
        after, _ = self._state()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(after, before - 500)

    def test_fixed_post_without_token_is_rejected(self):
        before, _ = self._state()
        response = self.client.post(
            "/csrf/fixed/transfer",
            data={"recipient": "Attacker demo account", "amount": "500"},
        )
        after, _ = self._state()
        self.assertEqual(response.status_code, 403)
        self.assertEqual(after, before)

    def test_fixed_post_with_valid_token_succeeds(self):
        before, token = self._state()
        response = self.client.post(
            "/csrf/fixed/transfer",
            data={
                "recipient": "Legitimate demo recipient",
                "amount": "100",
                "csrf_token": token,
            },
        )
        after, _ = self._state()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(after, before - 100)

    def test_fixed_post_with_wrong_token_is_rejected(self):
        before, _ = self._state()
        response = self.client.post(
            "/csrf/fixed/transfer",
            data={
                "recipient": "Attacker demo account",
                "amount": "500",
                "csrf_token": "not-the-session-token",
            },
        )
        after, _ = self._state()
        self.assertEqual(response.status_code, 403)
        self.assertEqual(after, before)


if __name__ == "__main__":
    unittest.main()
