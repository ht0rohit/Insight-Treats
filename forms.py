from flask_wtf import Form
from wtforms import TextField, PasswordField, SubmitField, BooleanField, TextAreaField, RadioField, FieldList, HiddenField
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
	pwd = PasswordField("Password", [validators.Required(), validators.NumberRange(min=6, max=20)])
	submit = SubmitField("SIGN UP")

class Contact(Form):
	fname = TextField("Name", [validators.Required()]) 
	emailid = TextField("Email ID", [validators.Required(),
        validators.Email("Please enter a valid E-mail address!")])
	text = TextAreaField("Message", [validators.Required()])
	submit = SubmitField("Leave Message")

class Edit(Form):
	#uname = TextField("User Name", [validators.Required()])
	iam = TextAreaField("I am", [validators.Required()])
	ii = TextAreaField("I", [validators.Required()])
	trends = TextAreaField("Trends", [validators.Required()])
	python = BooleanField("Python", [validators.optional()])
	cpp = BooleanField("C++", [validators.optional()])
	java = BooleanField("Java", [validators.optional()])
	js = BooleanField("JavaScript", [validators.optional()])
	iot = BooleanField("InternetOfThings", [validators.optional()])
	ml = BooleanField("Machine Learning", [validators.optional()])
	vr = BooleanField("Virtual Reality", [validators.optional()])
	ar = BooleanField("Augmented Reality", [validators.optional()])
	cc = BooleanField("Cloud Computing", [validators.optional()])
	eh = BooleanField("Information Security", [validators.optional()])
	proficiency = RadioField('Proficiency', [validators.Required()], choices = [('b','Novice'),('i','Intermediate'),('e','Expert')])
	uname = HiddenField()
	p_name = TextAreaField("Project", [validators.Required()])
	des = TextAreaField("Description", [validators.Required()])
	lang = TextAreaField("Languages used", [validators.Required()])
	github = TextAreaField("GitHub", [validators.Required(), validators.URL("Please enter a valid URL!")])
	submit = SubmitField("Save")

