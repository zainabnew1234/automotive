from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,BooleanField,SubmitField
from wtforms import validators
from wtforms.validators import DataRequired, Email, Length
from wtforms.widgets.core import PasswordInput


class Signup(FlaskForm):
     firstname = StringField("Firstname: ", validators=[DataRequired()])
     lastname = StringField("Lastname: ", validators=[DataRequired()])
     number = StringField("Phone number: ", validators=[DataRequired(),Length(min=11)])
     mail = StringField("Email: ",validators=[Email()])
     username=StringField("Username: ",validators=[DataRequired()])
     password = PasswordField("Password ",validators=[PasswordInput()])
     confword = PasswordField(" Confirm Password ",validators=[PasswordInput()])
     address =StringField("Address: ",validators=[DataRequired()])
     submit = SubmitField("Sign In")
     
     