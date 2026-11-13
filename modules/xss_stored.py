from flask import Blueprint, request, render_template

TITLE = "Cross-Site Scripting (Stored XSS)"
OWNER = "Srujan (M2)"
READY = True

bp = Blueprint('xss_stored', __name__, url_prefix='/xss_stored')

comments_db = []

@bp.route('/')
def index():
    return render_template('xss_stored/index.html')

@bp.route('/vulnerable', methods=['GET', 'POST'])
def vulnerable():
    if request.method == 'POST':
        # .strip() removes accidental whitespace, and 'if comment:' ensures it isn't empty
        comment = request.form.get('comment', '').strip()
        if comment:
            comments_db.append(comment)
    return render_template('xss_stored/vulnerable.html', comments=comments_db)

@bp.route('/secure', methods=['GET', 'POST'])
def secure():
    if request.method == 'POST':
        comment = request.form.get('comment', '').strip()
        if comment:
            comments_db.append(comment)
    return render_template('xss_stored/secure.html', comments=comments_db)