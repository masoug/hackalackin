from google.appengine.ext import db


class HackerProfile(db.Model):
    created = db.DateProperty(auto_now_add=True)
    email = db.EmailProperty(required=True)
    first_name = db.StringProperty(required=True)
    last_name = db.StringProperty(require=True)
    nickname = db.StringProperty()