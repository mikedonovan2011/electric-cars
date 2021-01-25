from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Regexp
from ecars.models import User

# maximum lengths come from the db models
username_validators = [DataRequired(), Length(min=2, max=20),
    Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0, 'Must begin with a letter then have letters, numbers, dots or underscores')]
email_validators = [DataRequired(), Email(), Length(max=120)]
password_validators = [DataRequired(), Length(max=60)]
confirm_password_validators = [DataRequired(), EqualTo('password')]


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=username_validators)
    email = StringField('Email', validators=email_validators)
    password = PasswordField('Password', validators=password_validators)
    confirm_password = PasswordField('Confirm Password', validators=confirm_password_validators)
    submit = SubmitField('Sign Up')

    # custom validator syntax: validate_<field name>
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=email_validators)
    password = PasswordField('Password', validators=password_validators)
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    username = StringField('Username', validators=username_validators)
    email = StringField('Email', validators=email_validators)
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')


class RequestResetForm(FlaskForm):
    email = StringField('Email', validators=email_validators)
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account with that email. You must register first.')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=password_validators)
    confirm_password = PasswordField('Confirm Password', validators=confirm_password_validators)
    submit = SubmitField('Reset Password')