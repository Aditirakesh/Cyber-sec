from flask import Flask, request, render_template_string

app = Flask(__name__)
# Simulates a database storing the persistent XSS payload
comments_db = [] 

# --- VULNERABLE IMPLEMENTATION ---
@app.route('/vulnerable', methods=['GET', 'POST'])
def vulnerable():
    if request.method == 'POST':
        comments_db.append(request.form.get('comment', ''))
    
    # Root Cause: The '|safe' filter disables Jinja2's auto-escaping, 
    # rendering the stored script directly in the DOM.
    template = '''
    <h2>Vulnerable Guestbook</h2>
    <form method="POST"><input type="text" name="comment"><input type="submit" value="Post"></form>
    <ul>
    {% for comment in comments_db %} 
        <li>{{ comment|safe }}</li> 
    {% endfor %}
    </ul>
    '''
    return render_template_string(template, comments_db=comments_db)


# --- MITIGATED IMPLEMENTATION ---
@app.route('/secure', methods=['GET', 'POST'])
def secure():
    if request.method == 'POST':
        comments_db.append(request.form.get('comment', ''))
    
    # Mitigation: Removed '|safe'. Framework auto-escaping converts 
    # <script> to &lt;script&gt;, neutralizing the payload.
    template = '''
    <h2>Secure Guestbook</h2>
    <form method="POST"><input type="text" name="comment"><input type="submit" value="Post"></form>
    <ul>
    {% for comment in comments_db %} 
        <li>{{ comment }}</li> 
    {% endfor %}
    </ul>
    '''
    return render_template_string(template, comments_db=comments_db)

if __name__ == '__main__':
    app.run(debug=True)
