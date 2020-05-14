from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, IntegerField, FloatField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from application.models import Users
from flask_login import current_user

class PostForm(FlaskForm):

    title = StringField("Title : ",
        validators = [
            DataRequired(),
            Length(min = 2, max = 100)
        ]
    )

    game = IntegerField("Game ID : ",
        validators = [
            DataRequired()
        ]
    )

    content = StringField("Content : ",
        validators = [
            DataRequired(),
            Length(min = 2, max = 500)
        ]
    )

    submit = SubmitField('Submit Content')

class NewGame(FlaskForm):
    game = StringField("Game : ",
        validators = [
            DataRequired(),
            Length(min = 1, max = 500)
        ]
    )

    description = StringField("Description : ",
        validators = [
            DataRequired(),
            Length(min = 2, max = 500)
        ]
    )

    submit = SubmitField('Submit Game')

class SellItem(FlaskForm):
    game = StringField("Game : ",
        validators = [
            DataRequired(),
            Length(min = 1, max = 500)
        ]
    )

    description = StringField("Description : ",
        validators = [
            DataRequired(),
            Length(min = 2, max = 500)
        ]
    )

    price = FloatField("Price : ",
        validators = [
            DataRequired()
        ]
    )

    submit = SubmitField('Sell Game')

class RegistrationForm(FlaskForm):
    user_name = StringField("User Name : ",
        validators = [
            DataRequired(),
            Length(min = 2, max = 30)
        ]
    )

    first_name = StringField("First Name : ",
        validators = [
            DataRequired(),
            Length(min = 2, max = 30)
        ]
    )

    last_name = StringField("Last Name : ",
        validators = [
            DataRequired(),
            Length(min = 2, max = 30)
        ]
    )

    email = StringField('Email : ',
        validators = [
            DataRequired(),
            Email()
        ]
    )
    password = PasswordField('Password : ',
        validators = [
            DataRequired(),
            Length(min = 8)
        ]
    )
    confirm_password = PasswordField('Confirm Password : ',
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
    email = StringField('Email : ',
        validators = [
            DataRequired(),
            Email()
        ]
    )

    password = PasswordField('Password : ',
        validators = [
            DataRequired()
        ]
    )

    remember = BooleanField('Remeber me')
    submit = SubmitField('Login')

class UpdateAccountForm(FlaskForm):
    first_name = StringField('First Name',
        validators=[
            DataRequired(),
            Length(min=4, max=30)
        ])
    last_name = StringField('Last Name',
        validators=[
            DataRequired(),
            Length(min=4, max=30)
        ])
    email = StringField('Email',
        validators=[
            DataRequired(),
            Email()
        ])
    submit = SubmitField('Update')

    def validate_email(self,email):
        if email.data != current_user.email:
            user = Users.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Email already in use')