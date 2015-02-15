from flask import Flask, render_template, redirect, request, url_for, make_response
from functools import wraps
from google.appengine.api import users
from google.appengine.ext import blobstore

from forms import ProfileEditBasicForm
from models import User, populate_entity, populate_form
from utils import header_to_blobkey, gravatar_url, gravatar_profile


app = Flask(__name__)
app.config['DEBUG'] = True

app.jinja_env.filters["gravatar_url"] = gravatar_url
app.jinja_env.filters["gravatar_profile"] = gravatar_profile

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


@app.route("/profile/")
@login_required
def profile():
    # TODO: in real life; use the user's supplied profile info
    user = User.all().filter("user_id =", users.get_current_user().user_id()).get()
    if not user:
        # prompt user to fill out profile
        user = None
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


@app.route("/logout/")
def logout():
    if not users.get_current_user():
        return redirect(url_for("index"))
    return render_template("logout.html", logout_url=users.create_logout_url(url_for("index")))

@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return render_template("404.html"), 404


# NOTE: Wanted to make a simple profile picture thing; but it is too complicated for now
# we'll just use gravatar
# @app.route("/profile/edit/pic/", methods=["POST", "GET"])
# @login_required
# def profile_edit_pic():
#     # upload with maximum 1mb image
#     upload_url = blobstore.create_upload_url(url_for("profile_edit_pic"), max_bytes_total=1000000)
#     if request.method == "POST":
#         # process for data
#         f = request.files['file']
#         blobkey = header_to_blobkey(f.headers["Content-Type"])
#         user = User.all().filter("user_id = ", users.get_current_user().user_id()).get()
#         user.profile_pic_blobkey = blobkey
#         user.put()
#         return render_template("profile_edit_pic.html", upload_url=upload_url, upload_success=True)
#     else:
#         # check that user exists
#         user = User.all().filter("user_id = ", users.get_current_user().user_id()).get()
#         if not user:
#             # redirect to make user create a profile first
#             return render_template("profile_edit_pic.html", no_profile=True)
#         else:
#             return render_template("profile_edit_pic.html", upload_url=upload_url)
#
# @app.route("/profile/pic/<bkey>")
# @login_required
# def profile_pic(bkey):
#     # serve user profile picture; otherwise just serve placeholder
#     user = User.all().filter("user_id = ", users.get_current_user().user_id()).get()
#     if not user or not user.profile_pic_blobkey:
#         return redirect("/static/images/nouser.jpg")
#     blob = blobstore.get(user.profile_pic_blobkey)
#     response = make_response(blob.open().read())
#     response.headers["Content-Type"] = blob.content_type
#     return response
