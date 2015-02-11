from flask import Flask, render_template, redirect, request, url_for
from functools import wraps
from google.appengine.api import users

from forms import ProfileEditBasicForm
from models import User, populate_entity, populate_form


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
    user = users.get_current_user()
    if user:
        h_user = User.all().filter("user_id =", user.user_id()).get()
        if h_user:
            user = h_user
        else:
            return redirect(url_for("profile_edit_basic"))
    return render_template("index.html", user=user,
                           login_url=users.create_login_url(url_for("index")),
                           logout_url=users.create_logout_url(url_for("index")))


@app.route("/profile/")
@login_required
def profile():
    # TODO: in real life; use the user's supplied profile info
    user = User.all().filter("user_id =", users.get_current_user().user_id()).get()
    if not user:
        return redirect(url_for("profile_edit_basic"))
    return render_template("profile.html", user=user,
                           logout_url=users.create_logout_url(url_for("index")))


@app.route("/profile/edit/basic/", methods=["POST", "GET"])
@login_required
def profile_edit_basic():
    if request.method == "POST":
        # validate and write new data
        form = ProfileEditBasicForm(request.form)
        if not form.validate():
            return render_template("profile_edit_basic.html",
                                   logout_url=users.create_logout_url(url_for("index")),
                                   form=form)

        # get user
        user = User.all().filter("user_id =", users.get_current_user().user_id()).get()
        if not user:
            # setup new user object
            user = User(user_id=users.get_current_user().user_id(),
                        email=form.email.data, first_name=form.first_name.data,
                        last_name=form.last_name.data)

        populate_entity(form, user, User)
        user.put()
        return render_template("profile_edit_basic.html",
                               logout_url=users.create_logout_url(url_for("index")),
                               form=form, update_success=True)
    else:
        # pre-populate existing fields
        form = ProfileEditBasicForm()
        user = User.all().filter("user_id = ", users.get_current_user().user_id()).get()
        if user:
            populate_form(form, user, User)
        else:
            form.email.data = users.get_current_user().email()
        return render_template("profile_edit_basic.html",
                               logout_url=users.create_logout_url(url_for("index")),
                               form=form)

@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return render_template("404.html"), 404
