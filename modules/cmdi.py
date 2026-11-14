"""OS Command Injection - In-band - owner: M3

Routes:
    /cmdi/          Hub page linking to vulnerable and fixed routes
    /cmdi/vuln/     Vulnerable version (ping with shell=True)
    /cmdi/fixed/    Secured version (argument-vector execution with shell=False)
"""
import ipaddress
import subprocess
from flask import Blueprint, render_template, request

OWNER = "Disha Gupta (M3)"
READY = True
TITLE = "OS Command Injection - In-band"
bp = Blueprint("cmdi", __name__, url_prefix="/cmdi")


def setup():
    """No database tables needed for OS command injection."""
    pass


def execute_ping_vuln(host: str) -> str:
    # INTENTIONALLY VULNERABLE: local lab only
    command = f"ping -n 1 -w 1000 {host}"
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=5,
            encoding="oem",
            errors="replace"
        )
        return (result.stdout or "") + (result.stderr or "")
    except subprocess.TimeoutExpired:
        return "Error: Diagnostic command timed out after 5 seconds."
    except OSError:
        return "Error: An internal operating system error occurred while executing the command."


def execute_ping_fixed(host: str) -> str:
    command_args = ["ping", "-n", "1", "-w", "1000", host]
    try:
        result = subprocess.run(
            command_args,
            shell=False,
            capture_output=True,
            text=True,
            timeout=5,
            encoding="oem",
            errors="replace"
        )
        return (result.stdout or "") + (result.stderr or "")
    except subprocess.TimeoutExpired:
        return "Error: Diagnostic command timed out after 5 seconds."
    except OSError:
        return "Error: An internal operating system error occurred while executing the command."


def validate_ip(host: str) -> str:
    # defence-in-depth, not the primary mitigation
    cleaned = host.strip()
    ipaddress.ip_address(cleaned)
    return cleaned


@bp.get("/")
def index():
    return render_template("cmdi/index.html")


@bp.get("/vuln/")
def vuln_get():
    return render_template("cmdi/vuln.html", host="", output="")


@bp.post("/vuln/")
def vuln_post():
    host = request.form.get("host", "")
    output = execute_ping_vuln(host)
    return render_template("cmdi/vuln.html", host=host, output=output)


@bp.get("/fixed/")
def fixed_get():
    return render_template("cmdi/fixed.html", error="", output="")


@bp.post("/fixed/")
def fixed_post():
    host = request.form.get("host", "")
    try:
        stripped_host = validate_ip(host)
    except ValueError:
        return render_template(
            "cmdi/fixed.html",
            error="Invalid input: Only valid IPv4 or IPv6 addresses are permitted.",
            output=""
        )

    output = execute_ping_fixed(stripped_host)
    return render_template("cmdi/fixed.html", error="", output=output)
