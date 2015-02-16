from google.appengine.api import users
from flask import url_for, redirect, render_template

from hackalackin import app
from models import User

@app.route("/")
def index():
    # TODO: In reality; query HackerProfile to get user nickname
    user = users.get_current_user()
    if user:
        # user is logged in via google
        h_user = User.all().filter("user_id =", user.user_id()).get()
        if h_user:
            # if user already filled out their profile...
            user = h_user
        else:
            # if user has not filled out their profile...
            user = None
    return render_template("index.html", user=user, guser=users.get_current_user(),
                           login_url=users.create_login_url(url_for("index")),
                           logout_url=users.create_logout_url(url_for("index")))


@app.route("/logout/")
def logout():
    if not users.get_current_user():
        return redirect(url_for("index"))
    return render_template("logout.html", logout_url=users.create_logout_url(url_for("index")))

@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return render_template("404.html"), 404
