from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField

class RegisterForm(FlaskForm):
    '''User registration form'''
    
    username = StringField('Username')
    email = EmailField('Email')
    first_name = StringField('First Name')
    last_name = StringField('Last Name')
    password = PasswordField('Password')