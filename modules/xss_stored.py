"""Stored XSS - owner: M2

Routes to build:
    /xss_stored/vuln/...   vulnerable version  (Table 2a, 2b)
    /xss_stored/fixed/...  same feature, one mitigation applied (Table 2d)
Keep everything for this variant inside THIS file, your own template
folder (templates/xss_stored/) and docs/M2_xss_stored.md.
"""
from flask import Blueprint

OWNER = "M2"
READY = False
TITLE = "Stored XSS"
bp = Blueprint("xss_stored", __name__, url_prefix="/xss_stored")


def setup():
    """Create your own tables / seed data here (use db.get_conn('xss_stored'))."""
    pass


@bp.route("/")
def home():
    return "Stored XSS - TODO (M2)"
