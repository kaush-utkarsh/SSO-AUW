import traceback, time, datetime
from user_agents import parse
import json,re, requests

def getCurrentTime():
	currTime=datetime.datetime.now()
	currTime=str(currTime)
	return currTime

def getSiblingOverview(db,mongo_db,cdate,referer):
	
	device_query = {"date":cdate, "referer":referer}
	device_data = db.select_db(mongo_db,"device_log",device_query)
	
	device_count=[]
	
	if len(device_data)==0:
		device_count.append({"label":"No Devices","data":1})
	else:
		for device in device_data:
			device_count.append({"label":device["device"],"data":device["count"]})

	city_query = {"date":cdate, "referer":referer}
	city_data = db.select_db(mongo_db,"city_counters",city_query)
	
	city_count=[]
	
	if len(city_data)==0:
		city_count.append({"label":"No City","data":1})
	else:
		for city in city_data:
			city_count.append({"label":city["city"],"data":city["total"]})

	day_query = {"date":cdate, "referer":referer}
	day_data = db.select_db(mongo_db,"date_day_split",day_query)
	
	day_count=[]
	
	if len(day_data)==0:
		day_count.append({"data" : 0, "label" : "00:00 - 02:00"})
		day_count.append({"data" : 0, "label" : "02:00 - 04:00"})
		day_count.append({"data" : 0, "label" : "04:00 - 06:00"})
		day_count.append({"data" : 0, "label" : "06:00 - 08:00"})
		day_count.append({"data" : 0, "label" : "08:00 - 10:00"})
		day_count.append({"data" : 0, "label" : "10:00 - 12:00"})
		day_count.append({"data" : 0, "label" : "12:00 - 14:00"})
		day_count.append({"data" : 0, "label" : "14:00 - 16:00"})
		day_count.append({"data" : 0, "label" : "16:00 - 18:00"})
		day_count.append({"data" : 0, "label" : "18:00 - 20:00"})
		day_count.append({"data" : 0, "label" : "20:00 - 22:00"})
		day_count.append({"data" : 0, "label" : "22:00 - 24:00"})
		
	else:
		for day in day_data:
			day_count.append({"data" : day["02AM"], "label" : "00:00 - 02:00"})
			day_count.append({"data" : day["04AM"], "label" : "02:00 - 04:00"})
			day_count.append({"data" : day["06AM"], "label" : "04:00 - 06:00"})
			day_count.append({"data" : day["08AM"], "label" : "06:00 - 08:00"})
			day_count.append({"data" : day["10AM"], "label" : "08:00 - 10:00"})
			day_count.append({"data" : day["12AM"], "label" : "10:00 - 12:00"})
			day_count.append({"data" : day["14AM"], "label" : "12:00 - 14:00"})
			day_count.append({"data" : day["16AM"], "label" : "14:00 - 16:00"})
			day_count.append({"data" : day["18AM"], "label" : "16:00 - 18:00"})
			day_count.append({"data" : day["20AM"], "label" : "18:00 - 20:00"})
			day_count.append({"data" : day["22AM"], "label" : "20:00 - 22:00"})
			day_count.append({"data" : day["24AM"], "label" : "22:00 - 24:00"})
			break;

	return_data={
					"devices":device_count,
					"cities":city_count,
					"day_time":day_count

				}

	return return_data

def getSiblingCities(db,mongo_db,cdate,referer):
	
	city_query = {"date":cdate, "referer":referer}
	city_data = db.select_db(mongo_db,"city_counters",city_query)
	
	citD=[]

	for cd in city_data:
		cD={}
		cD["city"]=cd["city"]
		cD["state"]=cd["state"]
		cD["country"]=cd["country"]
		cD["date"]=cd["date"]
		cD["morning"]=cd["morning"]
		cD["office"]=cd["office"]
		cD["evening"]=cd["evening"]
		cD["total"]=cd["total"]
		cD["referer"]=cd["referer"]
		citD.append(cD)

	return citD

def getLastSessions(db,mongo_db,referer):
	from pymongo import MongoClient

	sess_query = {"referer":referer}

	collection = mongo_db.get_collection("user_activity")
	if collection.count()>100:
		rows=collection.find(sess_query).skip(collection.count() - 100)
	else:
		rows=collection.find(sess_query)
	data=[]
	for row in rows:
		datum={}
		for r in row.keys():
			datum[r]=row[r]
		data.append(datum)

	citD=[]

	for cd in data:
		cD={}
		cD["ipAdd"]=cd["ipAdd"]
		cD["session_start"]=cd["session_start"]
		cD["country"]=cd["country"]
		cD["city"]=cd["city"]
		cD["state"]=cd["state"]
		cD["device_type"]=cd["device_type"]
		cD["os"]=cd["os"]
		cD["browser"]=cd["browser"]
		cD["referer"]=cd["referer"]
		citD.append(cD)

	return citD




def getSiblingDays(db,mongo_db,referer):
	
	tday=( datetime.date.today () - datetime.timedelta (days=0) ).strftime('%Y-%m-%d')
	d1 = ( datetime.date.today () - datetime.timedelta (days=1) ).strftime('%Y-%m-%d')
	d2 = ( datetime.date.today () - datetime.timedelta (days=2) ).strftime('%Y-%m-%d')
	d3 = ( datetime.date.today () - datetime.timedelta (days=3) ).strftime('%Y-%m-%d')
	d4 = ( datetime.date.today () - datetime.timedelta (days=4) ).strftime('%Y-%m-%d')
	d5 = ( datetime.date.today () - datetime.timedelta (days=5) ).strftime('%Y-%m-%d')
	d6 = ( datetime.date.today () - datetime.timedelta (days=6) ).strftime('%Y-%m-%d')
	d7 = ( datetime.date.today () - datetime.timedelta (days=7) ).strftime('%Y-%m-%d')
	d8 = ( datetime.date.today () - datetime.timedelta (days=8) ).strftime('%Y-%m-%d')
	d9 = ( datetime.date.today () - datetime.timedelta (days=9) ).strftime('%Y-%m-%d')
	d10 = ( datetime.date.today () - datetime.timedelta (days=10) ).strftime('%Y-%m-%d')
	d11 = ( datetime.date.today () - datetime.timedelta (days=11) ).strftime('%Y-%m-%d')

	counters = 	{
		tday:0,
		d1:0,
		d2:0,
		d3:0,
		d4:0,
		d5:0,
		d6:0,
		d7:0,
		d8:0,
		d9:0,
		d10:0,
		d11:0
	}

	ctr = [str(d11),str(d10),str(d9),str(d8),str(d7),str(d6),str(d5),str(d4),str(d3),str(d2),str(d1),str(tday)]

	day_query = {"referer":referer,
				"$or":[ 
						{"date":tday}, 
						{"date":d1}, 
						{"date":d2}, 
						{"date":d3}, 
						{"date":d4}, 
						{"date":d5}, 
						{"date":d6}, 
						{"date":d7}, 
						{"date":d8}, 
						{"date":d9}, 
						{"date":d10}, 
						{"date":d11}
					]
	}

	day_data = db.select_db(mongo_db,"date_day_split",day_query)
	
	citD=[]
	temp=[]

	for cd in day_data:
		cD={}
		tmp={}
		counters[cd["date"]]=cd["total"]
		tmp['label']=cd["date"]
		tmp['data']=cd["total"]
		temp.append(tmp)
	for key in ctr:
		citD.append([str(key),counters[key]])	

	return temp


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
		


		device_query = {"date":cdate, "device":device, "referer":referer}
		device_data = db.select_db(mongo_db,"device_log",device_query)
		
		if len(device_data)==0:

			ins_val={
						'date':cdate,
						'device':device,
						'count':1,
						"referer":referer
					}
		
			db.insert_db(mongo_db,"device_log",ins_val)
		
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

		city_query = {"date":cdate, "city":city, "state":state, "country":country, "referer":referer}
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
					"total":1,
					"referer":referer					
			}
		
			db.insert_db(mongo_db,"city_counters",ins_val)
		
		else:

			ins_val={
						timeQ:city_data[0][timeQ]+1,
						"total":city_data[0]["total"]+1					
					}
			db.update_db(mongo_db,"city_counters",ins_val,city_query)

		day_query = {"date":cdate, "referer":referer}
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
					"total":1,
					"referer":referer
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

