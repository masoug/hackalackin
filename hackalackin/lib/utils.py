"""
Utility functions
"""

from hashlib import md5
from urllib import urlencode
from functools import wraps
from google.appengine.api import users
from flask import redirect, request


def gravatar_url(email, size=150):
    hasher = md5()
    hasher.update(email.strip().lower())
    return "/".join(["https://www.gravatar.com/avatar",
                     hasher.hexdigest()+"?"+urlencode({"s": size, "d": "identicon"})])


def gravatar_profile(email):
    hasher = md5()
    hasher.update(email.strip().lower())
    return "/".join(["https://www.gravatar.com", hasher.hexdigest()])


def header_to_blobkey(header):
    headers = header.split(";")
    for entry in headers:
        if "blob-key" in entry:
            return entry.split("\"")[1]


def login_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if not users.get_current_user():
            return redirect(users.create_login_url(request.url))
        return func(*args, **kwargs)
    return decorated_view