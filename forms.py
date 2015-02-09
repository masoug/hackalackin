from wtforms import Form, BooleanField, StringField, validators


class LoginForm(Form):
    email = StringField("Email", [validators.Length(min=6, max=500), validators.InputRequired()])
