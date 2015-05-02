import traceback, time, datetime
from user_agents import parse
import json,re, requests

def getCurrentTime():
	currTime=datetime.datetime.now()
	currTime=str(currTime)
	return currTime

def user_log(db,mongo_db,session_st_end,username,ip,userAgent,sessionType,geo,referer):
	try:
		user_agent=parse(userAgent)
		browser = str(user_agent.browser.family)+', version: '+user_agent.browser.version_string
		os = str(user_agent.os.family)+', version: '+user_agent.os.version_string
		device = str(user_agent.device.family)
	except Exception, e:
		browser = ""
		os = ""
		device = ""

	currTime=getCurrentTime()
	if session_st_end=="session_start":
		gps_url= 'http://maps.google.com/maps/api/geocode/json?latlng='+geo.strip('()')+'&sensor=false'
		resp = requests.get(gps_url)
		response = str(resp.text).replace('\n','')
		resTxt=json.loads(response)
		addr=str(resTxt['results'][0]['formatted_address'])
		addrList=addr.split(',')
		country=(addrList[len(addrList)-1]).strip()
		city= (addrList[len(addrList)-3]).strip()
		state= (addrList[len(addrList)-2]).strip()
		pin=re.findall('\d+', state)
		state=state[:state.find(pin[0])].strip()
		cdate=str(time.strftime('%Y-%m-%d'))
		ctime=str(time.strftime('%H:%M:%S'))
		ins_val={
					'referer':referer,
					'username':username,
					'ipAdd':ip,
					'user_agent':userAgent,
					session_st_end:currTime,
					'date':cdate,
					'time':ctime,
					'session_type':sessionType,
					'geolocation':geo,
					"country":country,
					"city":city,
					"state":state,
					"device_type":device,
					"os":os,
					"browser":browser
				}
		db.insert_db(mongo_db,"user_activity",ins_val)

		sibling_query = {"sibling":referer}
		sibling_data = db.select_db(mongo_db,"siblings",sibling_query)
		
		if len(sibling_data)==0:

			ins_val={
						'sibling':referer
					}
		
			db.insert_db(mongo_db,"siblings",ins_val)
		


		device_query = {"date":cdate, "device":device}
		device_data = db.select_db(mongo_db,"device_log",device_query)
		
		if len(device_data)==0:

			ins_val={
						'date':cdate,
						'device':device,
						'count':1
					}
		
			db.insert_db(mongo_db,"device_data",ins_val)
		
		else:

			ins_val={
						'count':device_data[0]['count']+1					
					}
			db.update_db(mongo_db,"device_log",ins_val,device_query)

		cTimeObj = time.strptime(ctime,'%H:%M:%S')
		timeQ=""
		if(cTimeObj<time.strptime('10:00:00','%H:%M:%S')):
			timeQ="morning"
			timeQn1="office"
			timeQn2="evening"

		if(cTimeObj>=time.strptime('10:00:00','%H:%M:%S') and cTimeObj<time.strptime('19:00:00','%H:%M:%S')):
			timeQ="office"
			timeQn1="morning"
			timeQn2="evening"

		if(cTimeObj>=time.strptime('19:00:00','%H:%M:%S')):
			timeQ="evening"
			timeQn1="office"
			timeQn2="morning"

		city_query = {"date":cdate, "city":city, "state":state, "country":country}
		city_data = db.select_db(mongo_db,"city_counters",city_query)
		
		if len(city_data)==0:

			ins_val={
					"city":city,
					"state":state,
					"country":country,
					"date":cdate,
					timeQ:1,	# 00:00-10:00
					timeQn1:0,	# 10:00-19:00
					timeQn2:0,	# 19:00-23:59
					"total":1					
			}
		
			db.insert_db(mongo_db,"city_counters",ins_val)
		
		else:

			ins_val={
						timeQ:city_data[0][timeQ]+1,
						"total":city_data[0]["total"]+1					
					}
			db.update_db(mongo_db,"city_counters",ins_val,city_query)

		day_query = {"date":cdate}
		day_data = db.select_db(mongo_db,"date_day_split",day_query)

		if(cTimeObj<time.strptime('02:00:00','%H:%M:%S')):
			timeQn = "02AM"
			timeQn1 = "04AM"
			timeQn2 = "06AM"
			timeQn3 = "08AM"
			timeQn4 = "10AM"
			timeQn5 = "12AM"
			timeQn6 = "14AM"
			timeQn7 = "16AM"
			timeQn8 = "18AM"
			timeQn9 = "20AM"
			timeQn10 = "22AM"
			timeQn11 = "24AM"

		if(cTimeObj>=time.strptime('02:00:00','%H:%M:%S') and cTimeObj<time.strptime('04:00:00','%H:%M:%S')):
			timeQn1 = "02AM"
			timeQn = "04AM"
			timeQn2 = "06AM"
			timeQn3 = "08AM"
			timeQn4 = "10AM"
			timeQn5 = "12AM"
			timeQn6 = "14AM"
			timeQn7 = "16AM"
			timeQn8 = "18AM"
			timeQn9 = "20AM"
			timeQn10 = "22AM"
			timeQn11 = "24AM"

		if(cTimeObj>=time.strptime('04:00:00','%H:%M:%S') and cTimeObj<time.strptime('06:00:00','%H:%M:%S')):
			timeQn2 = "02AM"
			timeQn1 = "04AM"
			timeQn = "06AM"
			timeQn3 = "08AM"
			timeQn4 = "10AM"
			timeQn5 = "12AM"
			timeQn6 = "14AM"
			timeQn7 = "16AM"
			timeQn8 = "18AM"
			timeQn9 = "20AM"
			timeQn10 = "22AM"
			timeQn11 = "24AM"

		if(cTimeObj>=time.strptime('06:00:00','%H:%M:%S') and cTimeObj<time.strptime('08:00:00','%H:%M:%S')):
			timeQn3 = "02AM"
			timeQn1 = "04AM"
			timeQn2 = "06AM"
			timeQn = "08AM"
			timeQn4 = "10AM"
			timeQn5 = "12AM"
			timeQn6 = "14AM"
			timeQn7 = "16AM"
			timeQn8 = "18AM"
			timeQn9 = "20AM"
			timeQn10 = "22AM"
			timeQn11 = "24AM"

		if(cTimeObj>=time.strptime('08:00:00','%H:%M:%S') and cTimeObj<time.strptime('10:00:00','%H:%M:%S')):
			timeQn4 = "02AM"
			timeQn1 = "04AM"
			timeQn2 = "06AM"
			timeQn3 = "08AM"
			timeQn = "10AM"
			timeQn5 = "12AM"
			timeQn6 = "14AM"
			timeQn7 = "16AM"
			timeQn8 = "18AM"
			timeQn9 = "20AM"
			timeQn10 = "22AM"
			timeQn11 = "24AM"

		if(cTimeObj>=time.strptime('10:00:00','%H:%M:%S') and cTimeObj<time.strptime('12:00:00','%H:%M:%S')):
			timeQn5 = "02AM"
			timeQn1 = "04AM"
			timeQn2 = "06AM"
			timeQn3 = "08AM"
			timeQn4 = "10AM"
			timeQn = "12AM"
			timeQn6 = "14AM"
			timeQn7 = "16AM"
			timeQn8 = "18AM"
			timeQn9 = "20AM"
			timeQn10 = "22AM"
			timeQn11 = "24AM"

		if(cTimeObj>=time.strptime('12:00:00','%H:%M:%S') and cTimeObj<time.strptime('14:00:00','%H:%M:%S')):
			timeQn5 = "02AM"
			timeQn1 = "04AM"
			timeQn2 = "06AM"
			timeQn3 = "08AM"
			timeQn4 = "10AM"
			timeQn6 = "12AM"
			timeQn = "14AM"
			timeQn7 = "16AM"
			timeQn8 = "18AM"
			timeQn9 = "20AM"
			timeQn10 = "22AM"
			timeQn11 = "24AM"

		if(cTimeObj>=time.strptime('14:00:00','%H:%M:%S') and cTimeObj<time.strptime('16:00:00','%H:%M:%S')):
			timeQn5 = "02AM"
			timeQn1 = "04AM"
			timeQn2 = "06AM"
			timeQn3 = "08AM"
			timeQn4 = "10AM"
			timeQn7 = "12AM"
			timeQn6 = "14AM"
			timeQn = "16AM"
			timeQn8 = "18AM"
			timeQn9 = "20AM"
			timeQn10 = "22AM"
			timeQn11 = "24AM"

		if(cTimeObj>=time.strptime('16:00:00','%H:%M:%S') and cTimeObj<time.strptime('18:00:00','%H:%M:%S')):
			timeQn5 = "02AM"
			timeQn1 = "04AM"
			timeQn2 = "06AM"
			timeQn3 = "08AM"
			timeQn4 = "10AM"
			timeQn8 = "12AM"
			timeQn6 = "14AM"
			timeQn7 = "16AM"
			timeQn = "18AM"
			timeQn9 = "20AM"
			timeQn10 = "22AM"
			timeQn11 = "24AM"

		if(cTimeObj>=time.strptime('18:00:00','%H:%M:%S') and cTimeObj<time.strptime('20:00:00','%H:%M:%S')):
			timeQn5 = "02AM"
			timeQn1 = "04AM"
			timeQn2 = "06AM"
			timeQn3 = "08AM"
			timeQn4 = "10AM"
			timeQn9 = "12AM"
			timeQn6 = "14AM"
			timeQn7 = "16AM"
			timeQn8 = "18AM"
			timeQn = "20AM"
			timeQn10 = "22AM"
			timeQn11 = "24AM"

		if(cTimeObj>=time.strptime('20:00:00','%H:%M:%S') and cTimeObj<time.strptime('22:00:00','%H:%M:%S')):
			timeQn5 = "02AM"
			timeQn1 = "04AM"
			timeQn2 = "06AM"
			timeQn3 = "08AM"
			timeQn4 = "10AM"
			timeQn9 = "12AM"
			timeQn6 = "14AM"
			timeQn7 = "16AM"
			timeQn8 = "18AM"
			timeQn10 = "20AM"
			timeQn = "22AM"
			timeQn11 = "24AM"

		if(cTimeObj>=time.strptime('22:00:00','%H:%M:%S')):
			timeQn5 = "02AM"
			timeQn1 = "04AM"
			timeQn2 = "06AM"
			timeQn3 = "08AM"
			timeQn4 = "10AM"
			timeQn9 = "12AM"
			timeQn6 = "14AM"
			timeQn7 = "16AM"
			timeQn8 = "18AM"
			timeQn11 = "20AM"
			timeQn10 = "22AM"
			timeQn = "24AM"

		if len(day_data)==0:
			ins_val={
					"date":cdate,
					timeQn:1,	# 00:00 - 02:00
					timeQn1:0,	# 02:00 - 04:00
					timeQn2:0,	# 04:00 - 06:00
					timeQn3:0,	# 06:00 - 08:00
					timeQn4:0,	# 08:00 - 10:00
					timeQn5:0,	# 10:00 - 12:00
					timeQn6:0,	# 12:00 - 14:00
					timeQn7:0,	# 14:00 - 16:00
					timeQn8:0,	# 16:00 - 18:00
					timeQn9:0,	# 18:00 - 20:00
					timeQn10:0,	# 20:00 - 22:00
					timeQn11:0,	# 22:00 - 24:00
					"total":1
				}

			db.insert_db(mongo_db,"date_day_split",ins_val)
		
		else:

			ins_val={
						timeQn:day_data[0][timeQn]+1,
						"total":day_data[0]["total"]+1					
					}
			db.update_db(mongo_db,"date_day_split",ins_val,day_query)

	else:
		ins_val={
					session_st_end:currTime,
					'date':str(time.strftime('%Y-%m-%d')),
					'time':str(time.strftime('%H:%M:%S'))					
				}
		query = {
					'username':username,
					'ipAdd':ip,
					'user_agent':userAgent,
					'geolocation':geo,
					'referer':referer
				}
		db.update_db(mongo_db,"user_activity",ins_val,query)
	
	return "200"

