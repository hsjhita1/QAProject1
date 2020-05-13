from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from application.models import Users

class PostForm(FlaskForm):

    title = StringField("Title",
        validators = [
            DataRequired(),
            Length(min = 2, max = 100)
        ]
    )

    game = StringField("Game",
        validators = [
            DataRequired(),
            Length(min = 2, max = 100)
        ]
    )

    content = StringField("Content",
        validators = [
            DataRequired(),
            Length(min = 2, max = 500)
        ]
    )

    submit = SubmitField('Submit Content')

class RegistrationForm(FlaskForm):
    user_name = StringField("User Name",
        validators = [
            DataRequired(),
            Length(min = 2, max = 30)
        ]
    )

    first_name = StringField("First Name",
        validators = [
            DataRequired(),
            Length(min = 2, max = 30)
        ]
    )

    last_name = StringField("Last Name",
        validators = [
            DataRequired(),
            Length(min = 2, max = 30)
        ]
    )

    email = StringField('Email',
        validators = [
            DataRequired(),
            Email()
        ]
    )
    password = PasswordField('Password',
        validators = [
            DataRequired(),
            Length(min = 8)
        ]
    )
    confirm_password = PasswordField('Confirm Password',
        validators = [
            DataRequired(),
            EqualTo('password')
        ]
    )
    submit = SubmitField('Sign Up')

    def validate_email(self, email):
        user = Users.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already in use')


class LoginForm(FlaskForm):
    email = StringField('Email',
        validators = [
            DataRequired(),
            Email()
        ]
    )

    password = PasswordField('Password',
        validators = [
            DataRequired()
        ]
    )

    remember = BooleanField('Remeber me')
    submit = SubmitField('Login')