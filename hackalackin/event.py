from flask import render_template
from google.appengine.api import users

from hackalackin import app

@app.route("/event/<event_id>")
def event(event_id):
    return render_template("event.html")