from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo, Regexp
from wtforms.widgets import PasswordInput, HTMLString

class PasswordInputWithToggle(PasswordInput):
    def __init__(self, toggle_text='Show', **kwargs):
        super().__init__(**kwargs)
        self.toggle_text = toggle_text

    def __call__(self, field, **kwargs):
        kwargs.setdefault('id', field.id)
        html = super().__call__(field, **kwargs)
        return HTMLString(
            f'{html}'
            f'<button type="button" class="btn btn-outline-secondary toggle-password" onclick="togglePassword(\'{field.id}\')">'
            f'{self.toggle_text}'
            f'</button>'
        )


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()], widget=PasswordInputWithToggle())
    submit = SubmitField("Login")


class RegisterForm(FlaskForm):
    name = StringField("Name:", validators=[DataRequired(), Length(max=50, message='Name must have less than 50 characters')])
    phone = StringField("Phone No:", validators=[DataRequired(), Regexp('^(?=(?:\D*\d){4})(?!(?:\D*\d){16})\D*\d.*$', message="Phone number must be between 4 and 15 numbers")])
    email = StringField("Email:", validators=[DataRequired(), Email(message='Email must be in the email format. Ex: john@example.com')])
    password = PasswordField("Password:", validators=[DataRequired(), Length(12, 128, 'Password must be between 12 and 128 characters')], widget=PasswordInputWithToggle())
    confirm = PasswordField("Confirm Password:", validators=[EqualTo('password', message='Passwords must match')], widget=PasswordInputWithToggle())
    submit = SubmitField("Register")

class ChangePassForm(FlaskForm):
    cur_password = PasswordField("Current Password", validators=[DataRequired()], widget=PasswordInputWithToggle())
    new_password = PasswordField("New Password", validators=[DataRequired(), Length(12, 128, 'Password must be between 12 and 128 characters')], widget=PasswordInputWithToggle())
    confirm_password = PasswordField("Confirm New Password:", validators=[EqualTo('new_password', message='New Password must match')], widget=PasswordInputWithToggle())
    submit = SubmitField("ChangePass")
