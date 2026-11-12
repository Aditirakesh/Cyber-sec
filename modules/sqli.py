"""SQL Injection - Authentication bypass  |  owner: M1 (Aditi)

Routes
    /sqli/                  overview + payloads
    /sqli/vuln/login        VULNERABLE login (string concatenation)
    /sqli/fixed/login       FIXED login (parameterised query)

Own database: data/sqli.db  (created and seeded by setup()).
WARNING: intentionally vulnerable. Run on localhost only.
"""
from flask import Blueprint, render_template, request

from db import get_conn

OWNER = "M1 (Aditi)"
READY = True
TITLE = "SQL Injection - Authentication bypass"
OWNER = "Aditi Rakesh (M1)"
READY = True
bp = Blueprint("sqli", __name__, url_prefix="/sqli")


def setup():
    conn = get_conn("sqli")
    conn.execute(
        """CREATE TABLE IF NOT EXISTS users (
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               username TEXT UNIQUE NOT NULL,
               password TEXT NOT NULL,
               role TEXT NOT NULL
           )"""
    )
    if conn.execute("SELECT COUNT(*) FROM users").fetchone()[0] == 0:
        conn.executemany(
            "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
            [
                ("admin", "Sup3rS3cret!", "administrator"),
                ("alice", "alice123", "user"),
                ("bob", "bob123", "user"),
            ],
        )
    conn.commit()
    conn.close()


@bp.route("/")
def home():
    return render_template("sqli/home.html")


# ---------------------------------------------------------------------------
# (a) VULNERABLE IMPLEMENTATION
# ---------------------------------------------------------------------------
@bp.route("/vuln/login", methods=["GET", "POST"])
def vuln_login():
    ctx = {"mode": "vuln", "query": None, "user": None, "message": None}
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")

        # FLAW: user input is concatenated straight into the SQL string.
        query = (
            "SELECT * FROM users WHERE username = '" + username +
            "' AND password = '" + password + "'"
        )
        ctx["query"] = query

        conn = get_conn("sqli")
        try:
            row = conn.execute(query).fetchone()
            if row:
                ctx["user"] = dict(row)
            else:
                ctx["message"] = "Invalid username or password."
        except Exception as e:
            # Verbose error shown to the user (also helps an attacker).
            ctx["message"] = f"Database error: {e}"
        finally:
            conn.close()
    return render_template("sqli/login.html", **ctx)


# ---------------------------------------------------------------------------
# (d) MITIGATION: parameterised query (+ generic error message)
# ---------------------------------------------------------------------------
@bp.route("/fixed/login", methods=["GET", "POST"])
def fixed_login():
    ctx = {"mode": "fixed", "query": None, "user": None, "message": None}
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")

        # FIX: the SQL structure is fixed; input is sent separately as data.
        query = "SELECT * FROM users WHERE username = ? AND password = ?"
        ctx["query"] = query + f"    -- params: ({username!r}, {password!r})"

        conn = get_conn("sqli")
        try:
            row = conn.execute(query, (username, password)).fetchone()
            if row:
                ctx["user"] = dict(row)
            else:
                ctx["message"] = "Invalid username or password."
        except Exception:
            ctx["message"] = "Something went wrong. Please try again."
        finally:
            conn.close()
    return render_template("sqli/login.html", **ctx)
