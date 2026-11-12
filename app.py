"""Web Server Security assignment - shared app.

Every file in modules/ that defines a Flask Blueprint called `bp` is
registered automatically, so members never need to edit this file.
If a module defines setup(), it is called once at startup (create your
own tables / seed data there). Set READY = True in your module once your
vuln/fixed routes are built, so the home page badge updates.

Run:  python app.py      ->  http://127.0.0.1:5000
WARNING: this app is intentionally vulnerable. Run it on localhost only.
"""
import importlib
import pkgutil

from flask import Flask, render_template

import modules

app = Flask(__name__)
app.secret_key = "dev-only-not-a-real-secret"

loaded = []
for info in pkgutil.iter_modules(modules.__path__):
    mod = importlib.import_module(f"modules.{info.name}")
    if hasattr(mod, "setup"):
        mod.setup()
    if hasattr(mod, "bp"):
        app.register_blueprint(mod.bp)
        loaded.append({
            "name": info.name,
            "title": getattr(mod, "TITLE", info.name),
            "owner": getattr(mod, "OWNER", "TBD"),
            "ready": getattr(mod, "READY", False),
        })

loaded.sort(key=lambda m: m["name"])


@app.route("/")
def index():
    return render_template("index.html", modules=loaded)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
