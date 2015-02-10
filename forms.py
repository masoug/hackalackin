from wtforms import Form, BooleanField, StringField, validators, RadioField
from wtforms.fields.html5 import EmailField

strip_filter = lambda x: x.strip() if x else None


class ProfileEditBasicForm(Form):
    first_name = StringField("First Name", [validators.Length(min=2, max=500), validators.InputRequired()],
                             description="Your legal first name.", filters=[strip_filter])

    middle_name = StringField("Middle Name", [validators.Length(max=500)],
                              description="Optional middle name.", filters=[strip_filter])

    last_name = StringField("Last Name", [validators.Length(min=2, max=500), validators.InputRequired()],
                            description="Your legal last name.", filters=[strip_filter])

    nickname = StringField("Nickname", [validators.Length(max=500)],
                           description="What do you prefer to go by?", filters=[strip_filter])

    gender = RadioField("Gender", [validators.Optional()],
                        choices=[("male", "Male"), ("female", "Female"), ("other", "Other")])

    email = EmailField("Email", [validators.InputRequired(), validators.Length(min=6, max=500)],
                       description="Preferred email; we use this to contact you.", filters=[strip_filter])

    occupation = StringField("Occupation", [validators.Length(min=2, max=500), validators.InputRequired()],
                             description="One-word description of what you do i.e. student, employee, etc..",
                             filters=[strip_filter])

    affiliation = StringField("Affiliation", [validators.Length(min=4, max=500), validators.InputRequired()],
                              description="What company/school/etc... are you with/representing?",
                              filters=[strip_filter])

    field = StringField("Field", [validators.Length(max=500)],
                        description="What's your major/field of study/area of expertise?", filters=[strip_filter])

    location = StringField("Location", [validators.Length(max=500)],
                           description="(Country), City, State", filters=[strip_filter])

    hackathons = StringField("Hackathons", [validators.Length(max=500)],
                             description="Brief list of hackathons you've attended.", filters=[strip_filter])
