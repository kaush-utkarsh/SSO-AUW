from flask import Flask, render_template, session, redirect,url_for, flash, make_response, request, current_app
from db_handle import dbHandler
from functools import wraps
import traceback, time, datetime, hashlib
import geocoder
import subroutines, mongo_schema

app = Flask(__name__)
app.secret_key = 'guess'

# mongo parameters (major parameters not yet being used and are declared for future reference)
mongo_host="localhost" # host ip
mongo_port=3306 # host port Integer
mongo_poolSize=None # None or integer
mongo_queueMultiple=100 # Integer
mongo_queueTimeOut= 950 # Integer

# the database name
mongo_dtbs = "AUW" 
db = dbHandler()

# mongo connection
mongo_db = db.dbConn(mongo_host,mongo_port,mongo_poolSize,mongo_queueMultiple,mongo_queueTimeOut,mongo_dtbs)

# include the db schema so as to use throughout the db updates
auw_schema=mongo_schema.auw_schema 

def login_required(f):
	@wraps(f)
	def decorated_view(*args, **kwargs):
		if request.endpoint in app.view_functions:
			if 'username' not in session:
				return redirect('/')
		return f(*args, **kwargs)
	return decorated_view

@app.route('/signupAPI', methods = ['POST'])
def index():
	try:
		user_agent = request.headers.get('User-Agent')

		name = request.form['name']
		email = request.form['email']
		city = request.form['city']
		psword = request.form['psword']
		ip_addr = request.form['ip']
		geo = request.form['geo']

		psword = hashlib.md5(psword).hexdigest()
		session_start="session_start"
		
		query = {"email":email}
		user_data = db.select_db(mongo_db,"user_data",query)
		
		if len(user_data)==0:
		
			currTime=subroutines.getCurrentTime()
		
			ins_val={
						'name':name,
						'email':email,
						'username':email,
						'native_city':city,
						'current_city':city,
						'password':psword,
						'signup_type':"auw",
						'timestamp':currTime
					}
		
			db.insert_db(mongo_db,"user_data",ins_val)
		
			subroutines.user_log(db,mongo_db,session_start,email,ip_addr,user_agent,"SignUp",geo)
			
			session['name']=name
			session['username']=email
			session['email']=email
			session['ip']=ip_addr
			session['user_agent']=user_agent
			session['geo']=geo

			session['completeness']=len(ins_val.keys())*100/len(auw_schema.keys())
			return "True"
		
		else:
			return "False"
	except Exception,e:
		print traceback.format_exc()
		return "False"

@app.route('/signinAPI', methods = ['POST'])
def signinApi():
	try:
		user_agent = request.headers.get('User-Agent')
		ip_addr = request.form['ip']
		name = request.form['name']
		psword = request.form['psword']
		geo = request.form['geo']

		psword = hashlib.md5(psword).hexdigest()

		session_start="session_start"

		query={"username":name, "password":psword}
		user_data=db.select_db(mongo_db,"user_data",query)

		if len(user_data)!=0:

			for ud in user_data:

				name=ud['name']
				email=ud['email']
				username=ud['username']
				empty=0
				total=0

				for k in ud.keys():

					if ud[k]=="":
						empty=empty+1
					total=total+1

				break

			session['name']=name
			session['username']=username
			session['email']=email
			session['ip']=ip_addr
			session['user_agent']=user_agent
			session['geo']=geo
			session['completeness']=empty*100/total

			subroutines.user_log(db,mongo_db,session_start,email,ip_addr,user_agent,"SignIn",geo)
			
			return "True"
		else:
			return "False"
	except Exception,e:
		print traceback.format_exc()
		return "False"

@app.route('/')
@app.route('/login')
def login():
	return render_template('signin-1.html')

@app.route('/sign_out')
@login_required
def logout():
	session_end="session_end"
	subroutines.user_log(db,mongo_db,session_end,session['email'],session['ip'],session['user_agent'],"",session['geo'])			
	session.clear()
	return redirect('/')

@app.route('/auw_login')
def login_auw():
	return render_template('signin-2.html')


@app.route('/signup')
def signupPage():
	return render_template('signup-1.html')		

@app.route('/signup_proceed')
@login_required
def signupProceedPage():
	try:
		return render_template('signup-2.html',userName=session['name'],profile_Complete=session['completeness'])		
	except Exception,e:
		print traceback.format_exc()
		return render_template('signin-1.html')

if __name__ == '__main__':
	app.run(debug = True, port=8012	, host="0.0.0.0")
