from flask import Flask, render_template, session, redirect,url_for, flash, make_response, request, current_app
from db_handle import dbHandler
from functools import wraps
import traceback, time, datetime, hashlib, json
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
			if 'SignIn' not in session.keys():
				print session
				if 'username' not in session.keys():
					return redirect('/')
				else:
					return redirect('/password_set')
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
		source = request.form['source']
		referer = request.form['referer']

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
						'signup_type':source,
						'timestamp':currTime,
						'referer':referer
					}
		
			db.insert_db(mongo_db,"user_data",ins_val)
		
			subroutines.user_log(db,mongo_db,session_start,email,ip_addr,user_agent,"SignUp",geo,referer)
			
			session['source']=source
			
			session['name']=name
			session['username']=email
			session['email']=email
			session['ip']=ip_addr
			session['user_agent']=user_agent
			session['geo']=geo
			session['SignIn']=True
			session['referer']=referer
			session['completeness']=len(ins_val.keys())*100/len(auw_schema['user_data'].keys())
			return "True"
		
		else:
			return "False"
	except Exception,e:
		print traceback.format_exc()
		return "False"

@app.route('/setPwdAPI', methods = ['POST'])
def setPwdAPI():
	try:
		psword = request.form['psword']
		psword = hashlib.md5(psword).hexdigest()
				
		ins_val={
					'password':psword
				}

		db.update_db(mongo_db,"user_data",ins_val,{'username':session['username']})
				
		session['SignIn']=True
		return "True"
		
	except Exception,e:
		print traceback.format_exc()
		return "False"



@app.route('/socialSignIn', methods = ['POST'])
def social():
	try:
		user_agent = request.headers.get('User-Agent')
		name = request.form['name']
		email = request.form['email']
		ip_addr = request.form['ip']
		geo = request.form['geo']
		source = request.form['source']
		s_id = request.form['id']
		referer = request.form['referer']
		location = request.form['location']
		pic = request.form['picture']
		session_start="session_start"
		
		query = {"email":email}
		user_data = db.select_db(mongo_db,"user_data",query)
		
		pic_source=source[:-2]+"pic"

		if len(user_data)==0:
		
			currTime=subroutines.getCurrentTime()
		
			ins_val={
						'name':name,
						'email':email,
						'username':email,
						'signup_type':source,
						'timestamp':currTime,
						'referer':referer,
						'location':location,
						pic_source:pic,
						source:s_id
					}
		
			db.insert_db(mongo_db,"user_data",ins_val)
		
			subroutines.user_log(db,mongo_db,session_start,email,ip_addr,user_agent,"SignUp",geo,referer)
			
			session['name']=name
			session['username']=email
			session['email']=email
			session['ip']=ip_addr
			session['user_agent']=user_agent
			session['geo']=geo
			session['source']=source
			session['referer']=referer
			session['completeness']=len(ins_val.keys())*100/len(auw_schema['user_data'].keys())
			return "False"
		
		else:

			empty=0
			for ud in user_data:

				for k in ud.keys():
					if ud[k]!="":
						empty=empty+1
				break


			if user_data[0][source]!=s_id:
		
				ins_val={
						'location':location,
						pic_source:pic,
						source:s_id
						}
			
				db.update_db(mongo_db,"user_data",ins_val,{'username':email})
			
				subroutines.user_log(db,mongo_db,session_start,email,ip_addr,user_agent,"SignIn",geo,referer)
	
				session['source']=source
				
				session['name']=name
				session['username']=email
				session['email']=email
				session['ip']=ip_addr
				session['user_agent']=user_agent
				session['geo']=geo
				session['completeness']=empty*100/len(auw_schema['user_data'].keys())
				session['SignIn']=True
				session['referer']=referer
				return "True"
			
			else:
				subroutines.user_log(db,mongo_db,session_start,email,ip_addr,user_agent,"SignIn",geo,referer)

				session['source']=source
			
				session['name']=name
				session['username']=email
				session['email']=email
				session['ip']=ip_addr
				session['user_agent']=user_agent
				session['geo']=geo
				session['completeness']=empty*100/len(auw_schema['user_data'].keys())
				session['SignIn']=True
				session['referer']=referer
				return "True"


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
		referer = request.form['referer']
		psword = hashlib.md5(psword).hexdigest()

		session_start="session_start"

		query={"username":name, "password":psword}
		user_data=db.select_db(mongo_db,"user_data",query)

		if len(user_data)!=0:
			empty=0
			for ud in user_data:

				name=ud['name']
				email=ud['email']
				username=ud['username']

				for k in ud.keys():
					if ud[k]!="":
						empty=empty+1
				break

			session['source']="auw"
			session['name']=name
			session['username']=username
			session['email']=email
			session['ip']=ip_addr
			session['user_agent']=user_agent
			session['geo']=geo
			session['completeness']=empty*100/len(auw_schema['user_data'].keys())
			session['SignIn']=True
			session['referer']=referer
			subroutines.user_log(db,mongo_db,session_start,email,ip_addr,user_agent,"SignIn",geo,referer)
			
			return "True"
		else:
			return "False"
	except Exception,e:
		print traceback.format_exc()
		return "False"


@app.route('/changePasswordAPI', methods = ['POST'])
def changePasswordAPI():
	try:
		name = request.form['name']
		opsword = request.form['opwd']
		npsword = request.form['psword']

		opsword = hashlib.md5(opsword).hexdigest()
		npsword = hashlib.md5(npsword).hexdigest()

		session_start="session_start"

		query={"username":name, "password":opsword}
		user_data=db.select_db(mongo_db,"user_data",query)

		if len(user_data)!=0:
			ins_val={
					'password':npsword
				}

			db.update_db(mongo_db,"user_data",ins_val,{'username':name})			
	
			return "True"
		else:
			return "False"
	except Exception,e:
		print traceback.format_exc()
		return "False"


@app.route('/<sibling>/')
@app.route('/<sibling>/login')
def login(sibling=None):
	return render_template('signin-1.html',referer=sibling,linKey='75wicmi7s9jo0r',fbKey='1428557360782143',gKey='551417097677-2jb5r9hrf2h9lnskdaj89u29pc9daov5')

@app.route('/change_password')
def change_password():
	return render_template('change_password.html')

@app.route('/sign_out')
def logout():
	session_end="session_end"
	ref=session['referer']
	subroutines.user_log(db,mongo_db,session_end,session['email'],session['ip'],session['user_agent'],"",session['geo'],ref)			
	session.clear()
	return redirect('/'+ref+'/')

@app.route('/<sibling>/auw_login')
def login_auw(sibling=None):
	return render_template('signin-2.html',referer=sibling)

@app.route('/password_set')
def setPassword():
	return render_template('password_set.html')

@app.route('/<sibling>/signup')
def signupPage(sibling=None):
	return render_template('signup-1.html',referer=sibling)		

@app.route('/admin')
def admin():

	siblings=db.select_db(mongo_db,"siblings",{})

	sib_arr=[]

	for sib in siblings:
		sib_arr.append(sib['sibling'])

	cdate=str(time.strftime('%Y-%m-%d'))
		
	sibling_data=subroutines.getSiblingOverview(db,mongo_db,cdate,sib_arr[0])
	
	render_data={"siblings":sib_arr,"sibling_data":sibling_data}		

	return render_template('admin_page.html',data=json.dumps(render_data))

@app.route('/admin_cities')
def adminCity():

	siblings=db.select_db(mongo_db,"siblings",{})

	sib_arr=[]

	for sib in siblings:
		sib_arr.append(sib['sibling'])

	cdate=str(time.strftime('%Y-%m-%d'))
		
	sibling_data=subroutines.getSiblingCities(db,mongo_db,cdate,sib_arr[0])
	
	render_data={"siblings":sib_arr,"sibling_data":sibling_data}		

	return render_template('admin_city.html',data=json.dumps(render_data))

@app.route('/admin_days')
def adminDays():

	siblings=db.select_db(mongo_db,"siblings",{})

	sib_arr=[]

	for sib in siblings:
		sib_arr.append(sib['sibling'])
		
	sibling_data=subroutines.getSiblingDays(db,mongo_db,sib_arr[0])
	
	render_data={"siblings":sib_arr,"sibling_data":sibling_data}		

	return render_template('admin_day.html',data=json.dumps(render_data))

@app.route('/last_sessions')
def lastSessions():

	siblings=db.select_db(mongo_db,"siblings",{})

	sib_arr=[]

	for sib in siblings:
		sib_arr.append(sib['sibling'])
		
	sibling_data=subroutines.getLastSessions(db,mongo_db,sib_arr[0])
	
	render_data={"siblings":sib_arr,"sibling_data":sibling_data}		

	return render_template('last_sessions.html',data=json.dumps(render_data))



@app.route('/admin_login', methods = ['GET','POST'])
def adminLogin():
	
	if request.method == 'GET':
		return render_template('admin_login.html')		
	if request.method == 'POST':
		try:
			name = request.form['email']
			psword = request.form['psword']

			psword = hashlib.md5(psword).hexdigest()


			query={"email":name, "password":psword}
			user_data=db.select_db(mongo_db,"admin_user",query)

			if len(user_data)!=0:

				for ud in user_data:

					name=ud['name']
					email=ud['email']
					username=ud['email']
					break

				session['name']=name
				session['username']=username
				session['email']=email
				session['SignIn']=True
				
				return "True"
			else:
				return "False"
		except Exception,e:
			print traceback.format_exc()
			return "False"

@app.route('/admin_page_fetch', methods = ['POST'])
def adminPages():
	
	if request.method == 'POST':
		try:
			dt = request.form['date']
			referer = request.form['referer']
			page = request.form['page']

			if page == "Last 100 sessions":
				sibling_data=subroutines.getLastSessions(db,mongo_db,referer)
		
				render_data={"sibling_data":sibling_data}

			if page == "Hits per Days":
				sibling_data=subroutines.getSiblingDays(db,mongo_db,referer)
		
				render_data={"sibling_data":sibling_data}

			if page == "Hits per City":
				sibling_data=subroutines.getSiblingCities(db,mongo_db,dt,referer)
		
				render_data={"sibling_data":sibling_data}

			if page == "Overview":
				sibling_data=subroutines.getSiblingOverview(db,mongo_db,dt,referer)
		
				render_data={"sibling_data":sibling_data}

			return json.dumps(render_data)
		except Exception,e:
			print traceback.format_exc()
			return "False"



@app.route('/signup_proceed')
@login_required
def signupProceedPage():
	try:
		userData=db.select_db(mongo_db,"user_data",{"email":session['email']})
		pic=""

		if session["source"] != "auw":
			for uD in userData:
				print uD
				if uD[session["source"][:-2]+"pic"]!="":
					pic=uD[session["source"][:-2]+"pic"]
		print pic
		
		return render_template('signup-2.html',userName=session['name'],proPic=pic,profile_Complete=session['completeness'])		
	except Exception,e:
		print traceback.format_exc()
		return render_template('signin-1.html')

if __name__ == '__main__':
	# admin user creation:
	# psword = hashlib.md5("123456").hexdigest()
	# ins_val={
	# 					'name':"Utkarsh Kaushik",
	# 					'email':"utkarsh5929@gmail.com",
	# 					'username':"utkarsh5929@gmail.com",
	# 					'password':psword
	# 				}
		
	# db.insert_db(mongo_db,"admin_user",ins_val)
	# exit()
	app.run(debug = True, port=8012	, host="0.0.0.0")
