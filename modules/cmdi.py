"""OS Command Injection - In-band - owner: M3

Routes to build:
    /cmdi/vuln/...   vulnerable version  (Table 2a, 2b)
    /cmdi/fixed/...  same feature, one mitigation applied (Table 2d)
Keep everything for this variant inside THIS file, your own template
folder (templates/cmdi/) and docs/M3_cmdi.md.
"""
from flask import Blueprint

OWNER = "M3"
READY = False
TITLE = "OS Command Injection - In-band"
bp = Blueprint("cmdi", __name__, url_prefix="/cmdi")


def setup():
    """Create your own tables / seed data here (use db.get_conn('cmdi'))."""
    pass


@bp.route("/")
def home():
    return "OS Command Injection - In-band - TODO (M3)"
