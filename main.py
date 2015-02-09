from flask import Flask, render_template, redirect, request, url_for
from functools import wraps
from google.appengine.api import users


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
    # TODO: In reality; query HackerProfile to get user nickname
    return render_template("index.html", user=users.get_current_user(),
                           login_url=users.create_login_url(url_for("index")),
                           logout_url=users.create_logout_url(url_for("index")))


@app.route("/profile/")
@login_required
def profile():
    # TODO: in real life; use the user's supplied profile info
    return render_template("profile.html", user=users.get_current_user(),
                           logout_url=users.create_logout_url(url_for("index")))

@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return render_template("404.html"), 404
