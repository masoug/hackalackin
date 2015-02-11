from google.appengine.ext import db


class User(db.Model):
    # list of typical fields, but be careful of special fields (like user_id)
    PROP_LIST = ["email", "first_name", "middle_name", "last_name", "nickname", "gender",
                 "occupation", "affiliation", "field", "location", "hackathons"]

    user_id = db.StringProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)

    email = db.StringProperty(required=True)
    first_name = db.StringProperty(required=True)
    middle_name = db.StringProperty()
    last_name = db.StringProperty(required=True)
    nickname = db.StringProperty()
    gender = db.StringProperty()
    occupation = db.StringProperty()
    affiliation = db.StringProperty()
    field = db.StringProperty()
    location = db.StringProperty()
    hackathons = db.StringProperty()


def populate_entity(form, entity, entity_class):
    for prop in entity_class.PROP_LIST:
        setattr(entity, prop, getattr(form, prop).data)


def populate_form(form, entity, entity_class):
    for prop in entity_class.PROP_LIST:
        getattr(form, prop).data = getattr(entity, prop)
