from flask import Flask, render_template, url_for, redirect, flash, request, session, make_response
from forms import Login, Register, Contact
from profile import Profile
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
import secrets, mysql.connector, bleach, hashlib
from smtplib import SMTPRecipientsRefused

app = Flask(__name__)

mail=Mail(app)
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'insi8treats@gmail.com'
app.config['MAIL_PASSWORD'] = 'asdf1zxcv'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail = Mail(app)

s = URLSafeTimedSerializer('achristmascarol')

db = mysql.connector.connect(host = "localhost", user = "root", password = "aszxdfcv", database = "insight" )
c = db.cursor()
sql = """CREATE TABLE IF NOT EXISTS student (
	id INT AUTO_INCREMENT,
	name VARCHAR(25) NOT NULL,
	username VARCHAR(15) NOT NULL UNIQUE,
	email VARCHAR(35) NOT NULL UNIQUE,
	password VARCHAR(100) NOT NULL,
	active CHAR(1) DEFAULT 'n',
	PRIMARY KEY(id)
)"""
c.execute(sql)

def make_pwd_hash(uname, pwd):
	has = hashlib.sha256((uname + pwd + 'valardohaeris').encode('utf-8')).hexdigest()
	return has

def make_cookie_hash(uname):
	has = uname + '|' + hashlib.sha256((uname + 'valardohaeris').encode('utf-8')).hexdigest()
	return has

def validate_cookie(has):
	uname = has.split('|')[0]
	return uname

@app.route('/')
@app.route('/index/')
def index():
	'''Main page of Insight Treats'''
	log = Login()
	reg = Register()
	con = Contact()

	if request.cookies.get('userID'):
		userID = request.cookies.get('userID')
		username = validate_cookie(userID)
		if userID == make_cookie_hash(username):
			return redirect(url_for('student', username = username))
		else:
			return redirect(url_for('logout'))
	else:
		return render_template('index.html', log = log, reg = reg, con = con)

@app.route('/login/', methods = ['GET', 'POST'])
def login():
	log = Login()
	reg = Register()

	if request.method == 'POST':
		uname = request.form['uname']
		pwd = request.form['pwd']
		c.execute("select password from student where username = %s", (bleach.clean(uname),))
		result = c.fetchone()
		if result != None and result[0] == make_pwd_hash(uname, pwd):
			c.execute("select active from student where username = %s", (bleach.clean(uname),))
			result = c.fetchone()
			if result[0] == 'y':
				cook = request.form['cook']
				if cook:
					resp = make_response(redirect(url_for('student', username = uname)))
					has = make_cookie_hash(uname)
					resp.set_cookie('userID', has, max_age=2592000)
					return resp
			else:
				flash('Activate your account first with the link sent to your mail!')
				return redirect(url_for('login'))
		else:
			flash('Incorrect UserName or Password!')
			return redirect(url_for('login'))

	elif request.method == 'GET':
		if request.cookies.get('userID'):
			username = validate_cookie(userID)
			if userID == make_cookie_hash(username):
				return redirect(url_for('student', username = username))
			else:
				return redirect(url_for('logout'))
		return render_template('login.html', log = log, reg = reg)


@app.route('/<username>/')
def student(username):
	if request.cookies.get('userID'):
		userID = request.cookies.get('userID')
		if userID == make_cookie_hash(username):
			return render_template('success.html', username = username)
		else:
			redirect(url_for('logout'))
	else:
		return redirect(url_for('index'))

@app.route('/logout/')
def logout():
	#remove the username from the session if it is there
	resp = make_response(redirect(url_for('index')))
	resp.set_cookie('userID', "", expires=0)
	return resp

@app.route('/register/', methods = ['GET', 'POST'])
def register():
	log = Login()
	reg = Register()
	
	if request.method == 'POST':
		fname = request.form['fname']
		uname = request.form['uname']
		emailid = request.form['emailid']
		pwd = request.form['pwd']
		c.execute("select username from student where email = %s", (bleach.clean(emailid),))
		result = c.fetchone()
		if result != None:
			flash('E-mail ID already registered. Please SignIn!')
			return redirect(url_for('login'))
		else:			
			c.execute("select email from student where username = %s", (bleach.clean(uname),))
			result = c.fetchone()
			if result != None:
				flash('UserName not available!')
				return redirect(url_for('register'))
			else:
				try:
					has = make_pwd_hash(uname, pwd)
					c.execute("insert into student (name, username, email, password) values (%s, %s, %s, %s)", (bleach.clean(fname), bleach.clean(uname), bleach.clean(emailid), bleach.clean(has),))

					token = s.dumps(emailid, salt='email-confirm')
					msg = Message('Confirm E-mail', sender='insi8treats@gmail.com', recipients=[emailid])
					link = url_for('confirm_email', token = token, _external = True)
					msg.body = '''Valar Dohaeris!\n\nYou are now one step closer to making your work live on 'Insight Treats'. Activate your account by clicking on the following link: {}.
					\n\nOnce activated, complete your profile info...'''.format(link)
					mail.send(msg)

					db.commit()

					flash('A link has been sent to your E-mail ID. Activate your account with the same!')
					return render_template('s.html')
				except SMTPRecipientsRefused:
					db.rollback()
					flash('Enter a valid E-mail ID!')
					return redirect(url_for('register'))

	elif request.method == 'GET':
		if request.cookies.get('userID'):
			username = validate_cookie(userID)
			if userID == make_cookie_hash(username):
				return redirect(url_for('student', username = username))
			else:
				return redirect(url_for('logout'))
		return render_template('register.html', log = log, reg = reg)

@app.route('/confirm_email/<token>')
def confirm_email(token):
	try:
		emailid = s.loads(token, salt='email-confirm', max_age=86400)
		c.execute("update student set active = 'y' where email = %s", (bleach.clean(emailid),))
		db.commit()
		c.execute("select username from student where email = %s", (bleach.clean(emailid),))
		uname = c.fetchone()
		resp = make_response(redirect(url_for('index')))
		has = make_cookie_hash(uname[0])
		resp.set_cookie('userID', has, max_age=2592000)
		return resp

	except SignatureExpired:
		c.execute("delete from student where email = %s", (bleach.clean(email),))
		db.commit()
		return "<h1>The link has been expired. Try Signing Up again.</h1>"

@app.route('/log1/', methods = ['GET', 'POST'])
def log1():
	log = Login()

	return render_template('login.html', log = log)

@app.route('/reg1/', methods = ['GET', 'POST'])
def reg1():
	reg = Register()
	
	return render_template('register.html', reg = reg)

if __name__ == '__main__':
	app.secret_key = secrets.token_bytes(32)
	app.debug = True
	app.run(host = '0.0.0.0', port = 8000)