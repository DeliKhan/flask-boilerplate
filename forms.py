from flask_wtf import Form
from wtforms import StringField, PasswordField, FieldList, FormField, TextAreaField
from wtforms.validators import DataRequired, EqualTo, Length

# Set your classes here.


class RegisterForm(Form):
    username = StringField(
        'Username', validators=[DataRequired(), Length(min=5, max=25)]
    )
    email = StringField(
        'Email', validators=[DataRequired(), Length(min=6, max=40)]
    )
    password = PasswordField(
        'Password', validators=[DataRequired(), Length(min=6, max=40)]
    )
    confirm = PasswordField(
        'Repeat Password',
        [DataRequired(),
        EqualTo('password', message='Passwords must match')]
    )


class LoginForm(Form):
    username = StringField('Username', [DataRequired()])
    password = PasswordField('Password', [DataRequired()])


class ForgotForm(Form):
    email = StringField(
        'Email', validators=[DataRequired(), Length(min=6, max=40)]
    )

class QuestionForm(Form):
    question = StringField('Question', validators=[DataRequired(), Length(max=255)])

class SettingsForm(Form):
    questions = FieldList(FormField(QuestionForm), min_entries=1, max_entries=10)

# ...existing code...