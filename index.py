from flask import Flask, render_template, url_for, redirect, flash, request, session, make_response, jsonify, json
from forms import Login, Register, Contact, Edit
from profile import Profile, Profile2
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
import secrets, mysql.connector, bleach, hashlib, random, re
from smtplib import SMTPRecipientsRefused

app = Flask(__name__)

mail=Mail(app)
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'insi8treats@gmail.com'
app.config['MAIL_PASSWORD'] = 'asdfzxcv'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail = Mail(app)

s = URLSafeTimedSerializer('achristmascarol')

db = mysql.connector.connect(host = "localhost", user = "root", password = "aszxdfcv", database = "insight" )
c = db.cursor(buffered=True)
sql1 = """CREATE TABLE IF NOT EXISTS student (
	id INT AUTO_INCREMENT NOT NULL UNIQUE,
	name VARCHAR(25) NOT NULL,
	username VARCHAR(15),
	email VARCHAR(35) NOT NULL UNIQUE,
	password VARCHAR(100) NOT NULL,
	active CHAR(1) DEFAULT 'n',
	PRIMARY KEY(username)
)"""
c.execute(sql1)

sql2 = """CREATE TABLE IF NOT EXISTS profile (
	username VARCHAR(15) NOT NULL,
	iam VARCHAR(75) NOT NULL,
	ii VARCHAR(150) NOT NULL,
	trends VARCHAR(250) NOT NULL,
	python VARCHAR(4) DEFAULT 'n',
	cpp VARCHAR(4) DEFAULT 'n',
	java VARCHAR(4) DEFAULT 'n',
	js VARCHAR(4) DEFAULT 'n',
	iot VARCHAR(4) DEFAULT 'n',
	ml VARCHAR(4) DEFAULT 'n',
	vr VARCHAR(4) DEFAULT 'n',
	ar VARCHAR(4) DEFAULT 'n',
	cc VARCHAR(4) DEFAULT 'n',
	eh VARCHAR(4) DEFAULT 'n',
	proficiency CHAR(1) NOT NULL,
	github VARCHAR(50) NOT NULL,
	FOREIGN KEY(username) REFERENCES student(username)
)"""
c.execute(sql2)

sql3 = """CREATE TABLE IF NOT EXISTS project (
	username VARCHAR(15) NOT NULL,
	p_name VARCHAR(100) NOT NULL,
	des VARCHAR(250) NOT NULL,
	python VARCHAR(4) DEFAULT 'n',
	cpp VARCHAR(4) DEFAULT 'n',
	java VARCHAR(4) DEFAULT 'n',
	js VARCHAR(4) DEFAULT 'n',
	iot VARCHAR(4) DEFAULT 'n',
	ml VARCHAR(4) DEFAULT 'n',
	vr VARCHAR(4) DEFAULT 'n',
	ar VARCHAR(4) DEFAULT 'n',
	cc VARCHAR(4) DEFAULT 'n',
	eh VARCHAR(4) DEFAULT 'n',
	FOREIGN KEY(username) REFERENCES student(username)
)"""
c.execute(sql3)

#sql4 = """CREATE TABLE IF NOT EXISTS req (
#	id int NOT NULL,
#	details VARCHAR(255) NOT NULL
#)"""
#c.execute(sql4)


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

@app.route('/cmail/', methods = ['POST'])
def cmail():
	fname = request.form['fname']
	emailid = request.form['emailid']
	text = request.form['text']
	##print(fname)
	#print(emailid)
	print(text)
	ms = Message(fname, sender='insi8treats@gmail.com', recipients=['ht97kumarrk@gmail.com'])
	ms.body = text + "\n" + emailid;
	print(ms)
	mail.send(ms)
	return redirect(url_for('index'))


@app.route('/login/', methods = ['GET', 'POST'])
def login():
	log = Login()
	reg = Register()

	if request.method == 'POST':
		uname = request.form['uname']
		pwd = request.form['pwd']

		if(uname == "" or pwd == ""):
			flash('Please fill out all the fields!')
			return redirect(url_for('login'))

		c.execute("select password from student where username = %s", (bleach.clean(uname),))
		result = c.fetchone()
		if result != None and result[0] == make_pwd_hash(uname, pwd):
			c.execute("select active from student where username = %s", (bleach.clean(uname),))
			result = c.fetchone()
			if result[0] == 'y':
				cook = request.form.get('cook')
				if cook:
					c.execute("select iam from profile where username = %s", (bleach.clean(uname),))
					fetch = c.fetchone()
					if fetch != None:
						return "success"
					else:
						return "edit"	
			else:
				flash('Activate your account first with the link sent to your mail!')
				return redirect(url_for('login'))
		else:
			flash('Incorrect UserName or Password!')
			return redirect(url_for('login'))

	elif request.method == 'GET':
		return render_template('login.html', log = log, reg = reg)


@app.route('/edit/<uname>/')
def edit(uname):
	ed  = Edit()

	c.execute("select iam from profile where username = %s", (bleach.clean(uname),))
	fetch = c.fetchone()
	if fetch == None:
		return render_template('edit.html', uname = uname, ed = ed)
	else:
		return redirect(url_for('student', username = uname))


@app.route('/next/<uname>', methods = ['GET', 'POST'])
def next(uname):
	
	if request.method == 'POST':
		iam = request.form['iam']
		ii = request.form['ii']
		trends = request.form['trends']
		python = request.form.get('python')
		cpp = request.form.get('cpp')
		java = request.form.get('java')
		js = request.form.get('js')
		iot = request.form.get('iot')
		ml = request.form.get('ml')
		vr = request.form.get('vr')
		ar = request.form.get('ar')
		cc = request.form.get('cc')
		eh = request.form.get('eh')
		proficiency = request.form['proficiency']
		github = request.form['github']

		try:
			c.execute("insert into profile values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (bleach.clean(uname), bleach.clean(iam), bleach.clean(ii), bleach.clean(trends), python, cpp, java, js, iot, ml, vr, ar, cc, eh, bleach.clean(proficiency), bleach.clean(github),))
			db.commit()
			return redirect(url_for('success', uname = uname))
		except:
			db.rollback()
			return redirect(url_for('edit', uname = uname))


@app.route('/success/<uname>/')
def success(uname):
	resp = make_response(redirect(url_for('student', username = uname)))
	has = make_cookie_hash(uname)
	resp.set_cookie('userID', has, max_age=2592000)
	return resp


@app.route('/<username>/', methods = ['GET', 'POST'])
def student(username):
	#print(username)
	ed  = Edit(uname = username)

	if request.method == 'GET':
		if request.cookies.get('userID'):
			userID = request.cookies.get('userID')
			if userID == make_cookie_hash(username):
				c.execute("select id, name from student where username = %s", (bleach.clean(username),))
				res = c.fetchone()
				c.execute("select iam, ii, trends, python, cpp, java, js, iot, ml, vr, ar, cc, eh, proficiency, github from profile where username = %s", (bleach.clean(username),))
				res1 = c.fetchone()
				obj = res[0]
				obj_name = res[1]
				#obj_name_cap = obj_name.capitalize()
				obj_iam = res1[0]
				obj_ii = res1[1]
				obj_trends = res1[2]

				list1 = []

				obj_python = res1[3];	
				if obj_python == 'y':	
					list1.append('python')
				obj_cpp = res1[4];	
				if obj_cpp == 'y':	
					list1.append('cpp')
				obj_java = res1[5];	
				if obj_java == 'y':	
					list1.append('java')
				obj_js = res1[6];	
				if obj_js == 'y':	
					list1.append('js')
				obj_iot = res1[7];	
				if obj_iot == 'y':	
					list1.append('iot')
				obj_ml = res1[8];	
				if obj_ml == 'y':	
					list1.append('ml')
				obj_vr = res1[9];	
				if obj_vr == 'y':	
					list1.append('vr')
				obj_ar = res1[10];	
				if obj_ar == 'y':	
					list1.append('ar')
				obj_cc = res1[11];	
				if obj_cc == 'y':	
					list1.append('cc')
				obj_eh = res1[12];	
				if obj_eh == 'y':	
					list1.append('eh')
				obj_proficiency = res1[13]
				obj_github = res1[14]
				obj = Profile(obj_name, obj_iam, obj_ii, obj_trends,obj_python, obj_cpp, obj_java, obj_js, obj_iot, obj_ml, obj_vr, obj_ar, obj_cc, obj_eh, obj_proficiency, obj_github)
				c.execute("select name from student")
				stud = [item[0] for item in c.fetchall()]

				list2 = ['Python', 'Cpp', 'Java', 'JavaScript', 'InternetOfThings', 'MachineLearning', 'VirtualReality', 'AugmentedReality', 'CloudComputing', 'InformationSecurity']
				c.execute("select s.name from student s, profile p where s.username = p.username and p.python = 'y'")
				p1 = [item[0] for item in c.fetchall()]
				c.execute("select s.name from student s, profile p where s.username = p.username and p.cpp = 'y'")
				p2 = [item[0] for item in c.fetchall()]
				c.execute("select s.name from student s, profile p where s.username = p.username and p.java = 'y'")
				p3 = [item[0] for item in c.fetchall()]
				c.execute("select s.name from student s, profile p where s.username = p.username and p.js = 'y'")
				p4 = [item[0] for item in c.fetchall()]
				c.execute("select s.name from student s, profile p where s.username = p.username and p.iot = 'y'")
				p5 = [item[0] for item in c.fetchall()]
				c.execute("select s.name from student s, profile p where s.username = p.username and p.ml = 'y'")
				p6 = [item[0] for item in c.fetchall()]
				c.execute("select s.name from student s, profile p where s.username = p.username and p.vr = 'y'")
				p7 = [item[0] for item in c.fetchall()]
				print(p7)
				c.execute("select s.name from student s, profile p where s.username = p.username and p.ar = 'y'")
				p8 = [item[0] for item in c.fetchall()]
				c.execute("select s.name from student s, profile p where s.username = p.username and p.cc = 'y'")
				p9 = [item[0] for item in c.fetchall()]
				c.execute("select s.name from student s, profile p where s.username = p.username and p.eh = 'y'")
				p10 = [item[0] for item in c.fetchall()]

				c.execute("select username, iam, ii from profile where username != %s", (bleach.clean(username),))
				exe1 = c.fetchall()
				# a sequence or set will work here		# set the number to select here.
				exe = random.sample(exe1, 6)

				return render_template('success.html', username = username, stud = stud, obj = obj, ed = ed, exe = exe, list1 = list1, list2 = list2, p1=p1,p2=p2,p3=p3,p4=p4,p5=p5,p6=p6,p7=p7,p8=p8,p9=p9,p10=p10)
			else:
				redirect(url_for('logout'))
		else:
			return redirect(url_for('index'))

	else:
		iam = request.form['iam']
		ii = request.form['ii']
		trends = request.form['trends']
		python = request.form.get('python')
		cpp = request.form.get('cpp')
		java = request.form.get('java')
		js = request.form.get('js')
		iot = request.form.get('iot')
		ml = request.form.get('ml')
		vr = request.form.get('vr')
		ar = request.form.get('ar')
		cc = request.form.get('cc')
		eh = request.form.get('eh')
		proficiency = request.form['proficiency']
		github = request.form['github']

		c.execute("UPDATE profile SET iam=(%s) WHERE username=(%s)", (bleach.clean(iam), bleach.clean(username),))
		c.execute("UPDATE profile SET ii=(%s) WHERE username=(%s)", (bleach.clean(ii), bleach.clean(username),))
		c.execute("UPDATE profile SET trends=(%s) WHERE username=(%s)", (bleach.clean(trends), bleach.clean(username),))
		c.execute("UPDATE profile SET python=(%s) WHERE username=(%s)", (python, bleach.clean(username),))
		c.execute("UPDATE profile SET cpp=(%s) WHERE username=(%s)", (cpp, bleach.clean(username),))
		c.execute("UPDATE profile SET java=(%s) WHERE username=(%s)", (java, bleach.clean(username),))
		c.execute("UPDATE profile SET js=(%s) WHERE username=(%s)", (js, bleach.clean(username),))
		c.execute("UPDATE profile SET iot=(%s) WHERE username=(%s)", (iot, bleach.clean(username),))
		c.execute("UPDATE profile SET ml=(%s) WHERE username=(%s)", (ml, bleach.clean(username),))
		c.execute("UPDATE profile SET vr=(%s) WHERE username=(%s)", (vr, bleach.clean(username),))
		c.execute("UPDATE profile SET ar=(%s) WHERE username=(%s)", (ar, bleach.clean(username),))
		c.execute("UPDATE profile SET cc=(%s) WHERE username=(%s)", (cc, bleach.clean(username),))
		c.execute("UPDATE profile SET eh=(%s) WHERE username=(%s)", (eh, bleach.clean(username),))
		c.execute("UPDATE profile SET proficiency=(%s) WHERE username=(%s)", (proficiency, bleach.clean(username),))
		c.execute("UPDATE profile SET github=(%s) WHERE username=(%s)", (bleach.clean(github), bleach.clean(username),))
		db.commit()
		
		return redirect(url_for('student', username = username))

@app.route('/save/', methods = ['GET', 'POST'])
def save():
	ed  = Edit(uname = request.form['uname'])

		
	if request.method == 'POST':

		username = request.form['uname']

		c.execute("select python, cpp, java, js, iot, ml, vr, ar, cc, eh, proficiency, github from profile where username = %s", (bleach.clean(username),))
		res1 = c.fetchone()
		list1 = []

		obj_python = res1[0];	
		if obj_python == 'y':	
			list1.append('python')
		obj_cpp = res1[1];	
		if obj_cpp == 'y':	
			list1.append('cpp')
		obj_java = res1[2];	
		if obj_java == 'y':	
			list1.append('java')
		obj_js = res1[3];	
		if obj_js == 'y':	
			list1.append('js')
		obj_iot = res1[4];	
		if obj_iot == 'y':	
			list1.append('iot')
		obj_ml = res1[5];	
		if obj_ml == 'y':	
			list1.append('ml')
		obj_vr = res1[6];	
		if obj_vr == 'y':	
			list1.append('vr')
		obj_ar = res1[7];	
		if obj_ar == 'y':	
			list1.append('ar')
		obj_cc = res1[8];	
		if obj_cc == 'y':	
			list1.append('cc')
		obj_eh = res1[9];	
		if obj_eh == 'y':	
			list1.append('eh')

		p_name = request.form['p_name']
		des = request.form['des']
		python = request.form.get('python')
		cpp = request.form.get('cpp')
		java = request.form.get('java')
		js = request.form.get('js')
		print(js)
		iot = request.form.get('iot')
		ml = request.form.get('ml')
		vr = request.form.get('vr')
		ar = request.form.get('ar')
		cc = request.form.get('cc')
		eh = request.form.get('eh')
		c.execute("insert into project values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (bleach.clean(username), bleach.clean(p_name), bleach.clean(des), python, cpp, java, js, iot, ml, vr, ar, cc, eh,)) 
		db.commit()
		flash("Details successfully submitted!")
		return render_template('url.html', ed = ed, list1 = list1, username = username)

@app.route('/project/<username>/')
def project(username):
	print(username)
	c.execute("select p_name, des, python, cpp, java, js, iot, ml, vr, ar, cc, eh from project where username = %s", (bleach.clean(username),))
	pro = c.fetchall()
	print(pro)
	return render_template('project.html', pro = pro, username = username)
	#return jsonify(payload)

@app.route('/hover/<username>/')
def hover(username):
	print(username)
	c.execute("select username, lang from project")
	res = c.fetchall()
	exe = random.sample(res, 4)
	return render_template('hover.html', exe = exe, username = username)



@app.route('/id/<res>/')
def idd(res):
	c.execute("select username from student where name = %s", (bleach.clean(res),))
	prof1 = c.fetchone()
	#print(prof1)
	prof = prof1[0]
	#print(prof)
	return redirect(url_for('profile', prof = prof))

@app.route('/profile/<prof>/')
def profile(prof):
	c.execute("select id, name from student where username = %s", (bleach.clean(prof),))
	res1 = c.fetchone()
	c.execute("select iam, ii, trends from profile where username = %s", (bleach.clean(prof),))
	res2 = c.fetchone()
	obj = res1[0]
	obj_name = res1[1]
	obj_name_cap = obj_name.capitalize()
	obj_iam = res2[0]
	obj_ii = res2[1]
	obj_trends = res2[2]
	obj = Profile2(obj_name_cap, obj_iam, obj_ii, obj_trends)
	c.execute("select name from student")
	stud = [item[0] for item in c.fetchall()]

	return render_template('2.html', obj = obj, stud = stud, prof = prof)


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

		if(fname == "" or uname == "" or emailid == ""):
			flash('Please fill out all the fields!')
			return redirect(url_for('register'))
		elif(len(pwd) < 6 or len(pwd) > 20):
			flash('Password must be b/w 6-20 characters long!!')
			return redirect(url_for('register'))

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
					msg.body = '''Valar Dohaeris!\n\nYou are now one step closer to making your work live on 'Insight Treats'. Activate your account by clicking on the following link: {}
					\n\nOnce activated, complete your profile info...'''.format(link)
					mail.send(msg)

					db.commit()

					flash('A link has been sent to your E-mail ID. Activate your account with the same!')
					return redirect(url_for('login'))
				except SMTPRecipientsRefused:
					db.rollback()
					flash('Unknown Error! Please fill the form again.')
					return redirect(url_for('register'))

	elif request.method == 'GET':
		return render_template('register.html', log = log, reg = reg)


@app.route('/confirm_email/<token>')
def confirm_email(token):
	try:
		emailid = s.loads(token, salt='email-confirm', max_age=86400)
		c.execute("update student set active = 'y' where email = %s", (bleach.clean(emailid),))
		db.commit()
		c.execute("select username from student where email = %s", (bleach.clean(emailid),))
		un = c.fetchone()
		uname = un[0]
		
		resp = make_response(redirect(url_for('edit', uname = uname)))
		has = make_cookie_hash(uname)
		resp.set_cookie('userID', has, max_age=2592000)
		return resp

	except SignatureExpired:
		c.execute("delete from student where email = %s", (bleach.clean(email),))
		db.commit()
		return "<h1>The link has been expired. Try Signing Up again.</h1>"


if __name__ == '__main__':
	app.secret_key = secrets.token_bytes(32)
	app.run(host = '0.0.0.0', port = 8000, debug = True)