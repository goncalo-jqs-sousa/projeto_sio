from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo, Regexp


class LoginForm(FlaskForm):
	email = StringField("Email", validators=[DataRequired()])
	password = PasswordField("Password", validators=[DataRequired()])
	submit = SubmitField("Login")

class RegisterForm(FlaskForm):
	name = StringField("Name:", validators=[DataRequired(), Length(max=50)])
	phone = StringField("Phone No:", validators=[DataRequired(), Length(4, 15, 'Phone number must be between 4 and 15 numbers long'), Regexp("[0-9]+", message='Phone must be a number')])
	email = StringField("Email:", validators=[DataRequired(), Email()])
	password = PasswordField("Password:", validators=[
												DataRequired(),
												Length(8, 30, 'Password must be between 8 and 30 characters long'),
												Regexp(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[_\-&$@#!%^*+.]).*$', message= 'Password must contain a lowercase letter, an uppercase letter, a number and a valid symbol')])
	confirm = PasswordField("Confirm Password:", validators=[EqualTo('password', message='Passwords must match')])
	submit = SubmitField("Register")