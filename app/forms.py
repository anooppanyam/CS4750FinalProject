from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField

class EditAccountForm(FlaskForm):
    username = StringField('Username')
    password = StringField('Password')
    email = StringField('Email')
    submit = SubmitField('Save changes')


