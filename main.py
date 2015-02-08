from functools import wraps
from google.appengine.api import users
from flask import Flask, render_template, redirect, request
app = Flask(__name__)
app.config['DEBUG'] = True

# Note: We don't need to call run() since our application is embedded within
# the App Engine WSGI application server.


def login_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if not users.get_current_user():
            return redirect(users.create_login_url(request.url))
        return func(*args, **kwargs)
    return decorated_view

@app.route("/")
def index():
    if not users.get_current_user():
        return render_template("index.html")
    else:
        return redirect("/profile/")

@app.route('/profile/')
@login_required
def profile():
    return render_template("profile.html",
                           user=users.get_current_user(),
                           logout_url=users.create_logout_url("/"))

@app.route("/profile/new/")
def profile_new():
    return "So you want to make a new profile?"

@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, nothing at this URL.', 404
