from flask_wtf import Form
from wtforms import TextField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms import validators, ValidationError

class Login(Form):
	uname = TextField("User Name", [validators.Required()])
	pwd = PasswordField("Password", [validators.Required()])
	cook = BooleanField("Remember Me", default="y")
	submit = SubmitField("SIGN IN")

class Register(Form):
	fname = TextField("Name", [validators.Required()])
	uname = TextField("User Name", [validators.Required()])  
	emailid = TextField("Email ID", [validators.Required(),
        validators.Email("Please enter a valid E-mail address!")])
	pwd = PasswordField("Password", [validators.Required(), validators.Length(min=6, max=20)])
	submit = SubmitField("SIGN UP")

class Contact(Form):
	fname = TextField("Name", [validators.Required()]) 
	emailid = TextField("Email ID", [validators.Required(),
        validators.Email("Please enter a valid E-mail address!")])
	text = TextAreaField("Message", [validators.Required()])
	submit = SubmitField("Leave Message")