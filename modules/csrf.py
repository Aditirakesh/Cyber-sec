"""CSRF - POST-based forged action (auto-submitting form) - owner: M5.

This module is intentionally vulnerable only on /vuln/transfer for a
localhost-only academic demonstration. The fixed route uses a synchronizer
token stored in Flask's signed session cookie.
"""
import hmac
import secrets

from flask import Blueprint, abort, redirect, render_template, request, session, url_for

OWNER = "M5"
READY = True
TITLE = "CSRF - POST-based forged action"
bp = Blueprint("csrf", __name__, url_prefix="/csrf")

INITIAL_BALANCE = 10000


@bp.record_once
def configure_local_demo_cookie(state):
    """Allow the cross-site POST demo on localhost in modern browsers.

    The browser sends SameSite=None cookies only over a secure context.
    Modern browsers treat http://localhost as a potentially trustworthy
    origin. Open the legitimate app at http://localhost:5000 (not 127.0.0.1)
    and the attacker page at http://127.0.0.1:5000 to create distinct sites.
    This setting applies to the local educational app's Flask session cookie.
    """
    app = state.app
    app.config["SESSION_COOKIE_SAMESITE"] = "None"
    app.config["SESSION_COOKIE_SECURE"] = True
    app.config["SESSION_COOKIE_HTTPONLY"] = True


def _ensure_demo_state():
    if "csrf_balance" not in session:
        session["csrf_balance"] = INITIAL_BALANCE
        session["csrf_transfers"] = []
    if "csrf_token" not in session:
        session["csrf_token"] = secrets.token_urlsafe(32)


def _transfer(amount, recipient):
    session["csrf_balance"] = session.get("csrf_balance", INITIAL_BALANCE) - amount
    transfers = session.get("csrf_transfers", [])
    transfers.append({"amount": amount, "recipient": recipient})
    session["csrf_transfers"] = transfers


@bp.route("/")
def home():
    _ensure_demo_state()
    return render_template(
        "csrf/home.html",
        balance=session["csrf_balance"],
        transfers=session.get("csrf_transfers", []),
        token=session["csrf_token"],
    )


# ---------------------------------------------------------------------------
# (a) VULNERABLE IMPLEMENTATION: no CSRF token / intent validation.
# ---------------------------------------------------------------------------
@bp.route("/vuln/transfer", methods=["POST"])
def vuln_transfer():
    _ensure_demo_state()
    recipient = request.form.get("recipient", "Demo recipient")
    try:
        amount = int(request.form.get("amount", "0"))
    except (TypeError, ValueError):
        abort(400, "Amount must be an integer.")
    if amount <= 0 or amount > session["csrf_balance"]:
        abort(400, "Invalid amount.")
    # FLAW: a state-changing POST is accepted based only on the session cookie.
    _transfer(amount, recipient)
    return render_template(
        "csrf/result.html",
        mode="vuln",
        success=True,
        message=f"VULNERABLE endpoint accepted the transfer of ₹{amount} to {recipient}.",
        balance=session["csrf_balance"],
    )


# ---------------------------------------------------------------------------
# (d) MITIGATION: synchronizer token, compared in constant time.
# ---------------------------------------------------------------------------
@bp.route("/fixed/transfer", methods=["POST"])
def fixed_transfer():
    _ensure_demo_state()
    submitted_token = request.form.get("csrf_token", "")
    expected_token = session.get("csrf_token", "")
    if not submitted_token or not expected_token or not hmac.compare_digest(
        submitted_token, expected_token
    ):
        return render_template(
            "csrf/result.html",
            mode="fixed",
            success=False,
            message="BLOCKED: missing or invalid CSRF token. No transfer was made.",
            balance=session["csrf_balance"],
        ), 403

    recipient = request.form.get("recipient", "Demo recipient")
    try:
        amount = int(request.form.get("amount", "0"))
    except (TypeError, ValueError):
        abort(400, "Amount must be an integer.")
    if amount <= 0 or amount > session["csrf_balance"]:
        abort(400, "Invalid amount.")
    _transfer(amount, recipient)
    return render_template(
        "csrf/result.html",
        mode="fixed",
        success=True,
        message=f"PROTECTED endpoint accepted a valid-token transfer of ₹{amount} to {recipient}.",
        balance=session["csrf_balance"],
    )


@bp.route("/attacker/vuln")
def attacker_vuln():
    """Attacker page: auto-submits a forged POST to the vulnerable endpoint."""
    return render_template(
        "csrf/attacker.html",
        target_url="http://localhost:5000/csrf/vuln/transfer",
        heading="Attacker page — vulnerable endpoint",
    )


@bp.route("/attacker/fixed")
def attacker_fixed():
    """Same forged POST against the protected endpoint; it has no CSRF token."""
    return render_template(
        "csrf/attacker.html",
        target_url="http://localhost:5000/csrf/fixed/transfer",
        heading="Attacker page — protected endpoint",
    )


@bp.route("/reset", methods=["POST"])
def reset():
    _ensure_demo_state()
    submitted_token = request.form.get("csrf_token", "")
    if not submitted_token or not hmac.compare_digest(
        submitted_token, session.get("csrf_token", "")
    ):
        abort(403, "Valid CSRF token required to reset the demo.")
    session["csrf_balance"] = INITIAL_BALANCE
    session["csrf_transfers"] = []
    return redirect(url_for("csrf.home"))
