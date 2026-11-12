# M5 — CSRF: POST-based forged action

**Owner:** Pratishtha (M5)
**Variant:** Cross-Site Request Forgery (CSRF), POST-based forged action using an auto-submitting form.

## Scope and safety

This module is an intentionally vulnerable teaching demonstration. It uses a fake wallet balance stored in the Flask session; it does not connect to a bank, payment service, or real account. Run the application on localhost only. Do not deploy it publicly or test it against third-party systems.

## (a) Vulnerable implementation

**File:** `modules/csrf.py`
**Function:** `vuln_transfer()`
**Route:** `POST /csrf/vuln/transfer`

The route changes the user's demo balance after receiving a POST request. It validates the amount, but deliberately does not verify a CSRF token or otherwise establish that the request was intentionally initiated by the user.

## (b) Working exploit: auto-submitting POST form

**File:** `templates/csrf/attacker.html`
**Attacker page routes:**
- `/csrf/attacker/vuln`
- `/csrf/attacker/fixed`

The attacker page contains this form (the template uses the target URL supplied by the route):

```html
<form id="forged" method="post" action="http://localhost:5000/csrf/vuln/transfer">
  <input type="hidden" name="recipient" value="Attacker demo account">
  <input type="hidden" name="amount" value="500">
</form>
<script>document.getElementById("forged").submit();</script>
```

The browser submits the form automatically. To demonstrate the cross-site browser behaviour:

1. Start the app with `python app.py`.
2. Open the legitimate application at `http://localhost:5000/csrf/`.
3. Keep that browser session active.
4. Open `http://127.0.0.1:5000/csrf/attacker/vuln` in another tab. `localhost` and `127.0.0.1` are distinct sites for this local demonstration.
5. The attacker page auto-submits a POST to the legitimate `localhost` endpoint. Return to the CSRF home page and observe the demo balance decrease by ₹500.

The local demonstration configures the Flask session cookie with `SameSite=None; Secure; HttpOnly` so a modern browser can include it in this cross-site POST. Modern browsers treat `http://localhost` as a potentially trustworthy context. Use the exact hostnames above; if the browser or environment does not permit this local cookie behaviour, use the automated tests to verify endpoint behaviour and explain the browser-cookie requirement in the viva.

## (c) Root cause

The vulnerable endpoint treats possession of the authenticated session cookie as sufficient proof of user intent. Browsers may attach that cookie automatically to a cross-site form submission, so an attacker can cause a logged-in browser to issue an unwanted state-changing POST.

## (d) Mitigation implemented

**Mitigation:** Synchronizer CSRF token.

**File:** `modules/csrf.py`
**Function:** `fixed_transfer()`
**Route:** `POST /csrf/fixed/transfer`

The server generates a cryptographically unpredictable token with `secrets.token_urlsafe(32)`, stores it in the Flask session, and includes it as a hidden field in the legitimate form. On POST, the server compares the submitted token with the session token using `hmac.compare_digest`. Missing or incorrect tokens receive HTTP 403 and no transfer occurs.

To demonstrate the same forged payload against the fixed route:

1. Reset the wallet from the CSRF home page.
2. Open `http://127.0.0.1:5000/csrf/attacker/fixed`.
3. The auto-submitting form sends the same recipient and amount but intentionally has no `csrf_token` field.
4. The fixed endpoint responds with HTTP 403 and the balance remains unchanged.

A legitimate protected form includes the session token and succeeds.

**Evidence screenshot:** Save a screenshot of the browser showing the blocked request and unchanged balance as `docs/screenshots/M5_csrf_blocked.png`. This screenshot must be captured from the actual running application; it is not fabricated or pre-generated.

## (e) Other mitigations (theory)

- **SameSite cookies:** Configure session cookies with `SameSite=Lax` or `SameSite=Strict` where application requirements permit. This limits when browsers attach cookies to cross-site requests and can reduce CSRF exposure. It is defence in depth, not a replacement for tokens in all situations.
- **Re-authentication for sensitive actions:** Ask the user to re-enter a password or complete another authentication step before high-impact actions. This makes silent background requests insufficient for those actions.
- **Avoid state-changing GET requests:** GET should be safe and read-only. State changes should use POST/PUT/PATCH/DELETE and still receive CSRF protection. Changing the HTTP method alone does not prevent CSRF.

## Test cases

Automated tests are in `tests/test_csrf.py` and can be run with:

```bash
python -m unittest discover -s tests -v
```

The tests verify that:
- a POST without a token changes the vulnerable demo balance;
- a POST without a token is rejected by the fixed route with HTTP 403;
- a POST with the valid session token succeeds on the fixed route.

## Important demonstration note

The local attacker page uses two distinct hostnames (`localhost` and `127.0.0.1`) and a `SameSite=None; Secure` session cookie to model a cross-site browser request. Browser cookie policies vary. The automated tests verify the server-side flaw and mitigation independently of browser cookie policy.
