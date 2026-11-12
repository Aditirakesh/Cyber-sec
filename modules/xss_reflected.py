"""Reflected XSS - owner: M4

Routes to build:
    /xss_reflected/vuln/...   vulnerable version  (Table 2a, 2b)
    /xss_reflected/fixed/...  same feature, one mitigation applied (Table 2d)
Keep everything for this variant inside THIS file, your own template
folder (templates/xss_reflected/) and docs/M4_xss_reflected.md.
"""
from flask import Blueprint

OWNER = "M4"
READY = False
TITLE = "Reflected XSS"
bp = Blueprint("xss_reflected", __name__, url_prefix="/xss_reflected")


def setup():
    """Create your own tables / seed data here (use db.get_conn('xss_reflected'))."""
    pass


@bp.route("/")
def home():
    return "Reflected XSS - TODO (M4)"
