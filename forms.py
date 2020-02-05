from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import InputRequired, Email, Length


class CreateUserForm(FlaskForm):
    username = StringField('User Name',
                           validators=[
                                 InputRequired(),
                                 Length(min=1, max=20, 
                                        message="User Name must less than 20 characters.")])
    password = PasswordField('Password',
                             validators=[InputRequired()])
    email = StringField('Email',
                        validators=[
                                 InputRequired(),
                                 Email(),
                                 Length(min=1, max=50,
                                        message="Name must be less than 50 characters.")])
    first_name = StringField('First Name',
                             validators=[
                                 InputRequired(),
                                 Length(min=1, max=30, 
                                        message="Name must be 1 to 30 characters.")])
    last_name = StringField('Last Name',
                            validators=[
                                 InputRequired(),
                                 Length(min=1, max=30, 
                                        message="Name must be 1 to 30 characters.")])


class LoginForm(FlaskForm):
    username = StringField('User Name',
                           validators=[
                                 InputRequired()])
    password = PasswordField('Password',
                             validators=[InputRequired()])


class FeedbackForm(FlaskForm):
    title = StringField('Title',
                        validators=[
                            InputRequired(),
                            Length(min=1, max=100,
                                   message="Title must be less than 100 characters.")])
    content = TextAreaField('Content',
                          validators=[InputRequired()])