from wtforms import Form, BooleanField, StringField, validators, RadioField
from wtforms.fields.html5 import EmailField


class ProfileEditBasicForm(Form):
    first_name = StringField("First Name", [validators.Length(min=1, max=500), validators.InputRequired()],
                             description="Your legal first name.")

    last_name = StringField("Last Name", [validators.Length(min=1, max=500), validators.InputRequired()],
                            description="Your legal last name.")

    nickname = StringField("Nickname", [validators.Length(max=500)],
                           description="What do you prefer to go by?")

    gender = RadioField("Gender", [validators.InputRequired()],
                        choices=[("male", "Male"), ("female", "Female"), ("other", "Other")])

    email = EmailField("Email", [validators.InputRequired(), validators.Length(min=6, max=500)],
                       description="Preferred email; we use this to contact you.")

    email_confirm = EmailField("Confirm Email", [validators.EqualTo("email")],
                               description="Gotta make sure its right :D This is our only method of notifying you.")

    occupation = StringField("Occupation", [validators.Length(min=2, max=500), validators.InputRequired()],
                             description="One-word description of what you do i.e. student, employee, etc..")

    affiliation = StringField("Affiliation", [validators.Length(min=4, max=500), validators.InputRequired()],
                              description="What company/school/etc... are you with/representing?")

    field = StringField("Field", [validators.Length(max=500)],
                        description="What's your major/field of study/area of expertise?")

    location = StringField("Location", [validators.Length(max=500)],
                           description="(Country), City, State")

    hackathons = StringField("Hackathons", [validators.Length(max=500)],
                             description="Brief list of hackathons you've attended.")


class LoginForm(Form):
    email = StringField("Email", [validators.Length(min=6, max=500), validators.InputRequired()])
