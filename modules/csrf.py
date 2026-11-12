"""CSRF - POST-based - owner: M5

Routes to build:
    /csrf/vuln/...   vulnerable version  (Table 2a, 2b)
    /csrf/fixed/...  same feature, one mitigation applied (Table 2d)
Keep everything for this variant inside THIS file, your own template
folder (templates/csrf/) and docs/M5_csrf.md.
"""
from flask import Blueprint

OWNER = "M5"
READY = False
TITLE = "CSRF - POST-based"
bp = Blueprint("csrf", __name__, url_prefix="/csrf")


def setup():
    """Create your own tables / seed data here (use db.get_conn('csrf'))."""
    pass


@bp.route("/")
def home():
    return "CSRF - POST-based - TODO (M5)"
